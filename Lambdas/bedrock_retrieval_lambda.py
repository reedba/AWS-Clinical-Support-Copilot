import boto3
import json
import logging
import os

"""
LAMBDA FUNCTION OVERVIEW
========================

This Lambda orchestrates queries between your Gradio frontend and Bedrock Knowledge Base.
It retrieves grounded answers from your healthcare policy documents.

FLOW:
1. User sends question via API Gateway → Lambda
2. Lambda sends question to Bedrock Knowledge Base
3. Bedrock performs vector search on your S3 documents
4. Lambda combines results and formats structured JSON response
5. Response returns to frontend with answer + sources

RESPONSE MODES:
- "policy_answer": Full detailed answer from documents
- "admin_summary": Truncated to 500 chars for quick staff reviews

The function is stateless and handles each request independently.
All requests are logged to CloudWatch for observability and compliance.
"""

# ===== INITIALIZATION =====
# boto3: AWS SDK for Python - allows us to call AWS services
# bedrock_client: Connection to Bedrock service in us-east-1 region
# KNOWLEDGE_BASE_ID: Your KB ID (SA1GTRJROV) - where Bedrock searches for answers
# logger: Captures all function events for CloudWatch monitoring

bedrock_client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

# Knowledge Base configuration
KNOWLEDGE_BASE_ID = 'SA1GTRJROV'
MODEL_ID = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-haiku-20240307-v1:0')
MAX_CONTEXT_CHARS = 3000
ALLOW_RAW_FALLBACK = os.getenv('ALLOW_RAW_FALLBACK', 'false').lower() == 'true'
SYSTEM_PROMPT = (
    "You are a clinical operations policy assistant. "
    "Summarize and answer based only on the provided context. "
    "Do not copy large passages verbatim. "
    "If the answer is not in the context, say so."
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def build_context(results):
    chunks = []
    for result in results:
        text = result.get('content', {}).get('text', '')
        if text:
            chunks.append(text.strip())
    context = "\n\n".join(chunks)
    return context[:MAX_CONTEXT_CHARS]


def extract_source(result):
    metadata = result.get('metadata', {}) or {}
    source = metadata.get('source') or metadata.get('filename')
    if source:
        return source
    location = result.get('location', {}) or {}
    s3_location = location.get('s3Location', {}) or {}
    uri = s3_location.get('uri')
    if uri:
        return uri.split('/')[-1]
    return 'Unknown'


def call_bedrock_summary(prompt, context_text, request_type):
    if request_type == 'admin_summary':
        instruction = (
            "Summarize the context for front desk staff in 4-6 bullet points. "
            "Each bullet must start with '- '. "
            "Use only the provided context. If the answer is not in context, say so."
        )
    else:
        instruction = (
            "Answer the user question using only the provided context. "
            "Be concise and policy-focused. Limit to 6 sentences max. "
            "If the answer is not in context, say so."
        )

    user_text = (
        f"System:\n{SYSTEM_PROMPT}\n\n"
        f"User question:\n{prompt}\n\n"
        f"Context:\n{context_text}\n\n"
        f"Instruction:\n{instruction}\n"
    )

    if MODEL_ID.startswith('anthropic.'):
        response = bedrock_runtime.invoke_model(
            modelId=MODEL_ID,
            contentType='application/json',
            accept='application/json',
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "system": SYSTEM_PROMPT,
                    "max_tokens": 300,
                    "temperature": 0.2,
                    "messages": [
                        {"role": "user", "content": [{"type": "text", "text": user_text}]}
                    ],
                }
            ),
        )

        raw_body = response.get('body')
        model_payload = json.loads(raw_body.read()) if hasattr(raw_body, 'read') else json.loads(raw_body)
        content = model_payload.get('content', [])
        if content and isinstance(content, list):
            return "".join([item.get('text', '') for item in content]).strip()
        return ""

    response = bedrock_runtime.invoke_model(
        modelId=MODEL_ID,
        contentType='application/json',
        accept='application/json',
        body=json.dumps(
            {
                "inputText": user_text,
                "textGenerationConfig": {
                    "maxTokenCount": 300,
                    "temperature": 0.2,
                    "topP": 0.9,
                },
            }
        ),
    )

    raw_body = response.get('body')
    model_payload = json.loads(raw_body.read()) if hasattr(raw_body, 'read') else json.loads(raw_body)
    results = model_payload.get('results', [])
    if results and isinstance(results, list):
        return results[0].get('outputText', '').strip()
    return ""


def lambda_handler(event, context):
    """
    MAIN HANDLER - Called by AWS Lambda runtime on each invocation
    
    Parameters:
    - event: The incoming request (JSON from API Gateway or test)
    - context: Runtime info (request ID, memory, etc.)
    
    Expected event format:
    {
        "prompt": "What documents are required for a new patient?",
        "request_type": "policy_answer"  # or "admin_summary"
    }
    """
    try:
        # ===== STEP 1: PARSE INPUT =====
        # Extract the user's question and desired response mode
        # Handle both direct dict and stringified JSON from API Gateway
        body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event
        prompt = body.get('prompt', '')
        request_type = body.get('request_type', 'policy_answer')
        
        # Validate: prompt is required to query Bedrock
        if not prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'prompt is required'})
            }
        
        # ===== STEP 2: QUERY BEDROCK KNOWLEDGE BASE =====
        # Call Bedrock's retrieve API with the user's prompt
        # - knowledgeBaseId: Points to your KB with your healthcare documents
        # - numberOfResults: Return top 5 most relevant documents (tunable)
        # - retrievalQuery.text: The user's actual question
        # Bedrock performs semantic search (vector similarity) on your documents
        response = bedrock_client.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 3
                }
            },
            retrievalQuery={'text': prompt}
        )
        
        # ===== STEP 3: PROCESS BEDROCK RESULTS =====
        # Extract the documents Bedrock found, combine them into one answer,
        # and pull out the source filenames for citation
        results = response.get('retrievalResults', [])
        answer = ''
        sources = []
        
        if results:
            # Combine all retrieved document snippets into one context block
            context_text = build_context(results)
            # Extract source filenames from metadata (which documents were used)
            # Use set() to remove duplicate sources
            sources = list({extract_source(result) for result in results})

            try:
                answer = call_bedrock_summary(prompt, context_text, request_type)
            except Exception as summary_error:
                logger.exception("Summary generation failed.")
                if ALLOW_RAW_FALLBACK:
                    answer = context_text
                else:
                    answer = (
                        "Summary generation failed. Please try again later or "
                        "check Lambda logs for details."
                    )
        else:
            # If no results, provide clear feedback
            answer = "No relevant documents found for your query."
        
        # ===== STEP 4: FORMAT RESPONSE BASED ON REQUEST TYPE =====
        # Two response modes support different use cases:
        # - admin_summary: Quick 500-char answers for fast decision-making (UI dropdowns, mobile)
        # - policy_answer: Full detailed answer for complete policy reference
        if request_type == 'admin_summary':
            structured_response = {
                'response_type': 'admin_summary',
                'summary': answer,
                'sources': sources,
                'confidence_note': 'Grounded in internal policy documents.'
            }
        else:  # policy_answer (default)
            structured_response = {
                'response_type': 'policy_answer',
                'answer': answer,
                'sources': sources,
                'confidence_note': 'Grounded in internal policy documents.'
            }
        
        # Log successful execution for monitoring
        logger.info(f"Successfully retrieved response for prompt: {prompt[:50]}")
        
        # ===== STEP 5: RETURN RESPONSE =====
        # Return HTTP 200 with JSON body
        # API Gateway and frontend will parse this response
        return {
            'statusCode': 200,
            'body': json.dumps(structured_response),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    
    # ===== ERROR HANDLING =====
    # If anything breaks (Bedrock connection fails, permission denied, etc.),
    # catch it, log for debugging, and return HTTP 500 with error details
    except Exception as e:
        logger.error(f"Error in Lambda handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }