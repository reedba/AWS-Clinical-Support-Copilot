import boto3
import json
import logging

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

# Knowledge Base configuration
KNOWLEDGE_BASE_ID = 'SA1GTRJROV'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
                    'numberOfResults': 5
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
            # Combine all retrieved document snippets into one cohesive answer
            answer = ' '.join([result['content']['text'] for result in results])
            # Extract source filenames from metadata (which documents were used)
            # Use set() to remove duplicate sources
            sources = list(set([
                result['metadata'].get('source', result['metadata'].get('filename', 'Unknown'))
                for result in results if 'metadata' in result
            ]))
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
                'summary': answer[:500],  # Truncate to 500 chars for quick consumption
                'sources': sources,
                'confidence_note': 'Grounded in internal policy documents.'
            }
        else:  # policy_answer (default)
            structured_response = {
                'response_type': 'policy_answer',
                'answer': answer,  # Full untruncated answer
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