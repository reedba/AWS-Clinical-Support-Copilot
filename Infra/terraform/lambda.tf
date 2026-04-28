# Package the v2 Lambda code from repository source.
data "archive_file" "bedrock_lambda_v2" {
  type        = "zip"
  source_file = "${path.module}/../../Lambdas/bedrock_retrieval_lambda_v2.py"
  output_path = "${path.module}/lambda_packages/bedrock_retrieval_lambda_v2.zip"
}

# IAM role for Lambda execution.
resource "aws_iam_role" "bedrock_lambda_v2" {
  name = "bedrock-retrieval-lambda-v2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

# Basic logging permissions for CloudWatch.
resource "aws_iam_role_policy_attachment" "bedrock_lambda_v2_logs" {
  role       = aws_iam_role.bedrock_lambda_v2.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Minimum permissions for Bedrock retrieve + invoke.
resource "aws_iam_policy" "bedrock_lambda_v2_bedrock" {
  name = "bedrock-retrieval-lambda-v2-bedrock"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:Retrieve",
          "bedrock:InvokeModel"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bedrock_lambda_v2_bedrock" {
  role       = aws_iam_role.bedrock_lambda_v2.name
  policy_arn = aws_iam_policy.bedrock_lambda_v2_bedrock.arn
}

# Lambda entrypoint for retrieval + LLM summarization.
resource "aws_lambda_function" "bedrock_lambda_v2" {
  function_name = "bedrock-retrieval-lambda-v2"
  role          = aws_iam_role.bedrock_lambda_v2.arn
  handler       = "bedrock_retrieval_lambda_v2.lambda_handler"
  runtime       = "python3.11"

  filename         = data.archive_file.bedrock_lambda_v2.output_path
  source_code_hash = data.archive_file.bedrock_lambda_v2.output_base64sha256

  memory_size = 512
  timeout     = 30

  environment {
    variables = {
      BEDROCK_MODEL_ID   = "anthropic.claude-3-haiku-20240307-v1:0"
      ALLOW_RAW_FALLBACK = "false"
      KNOWLEDGE_BASE_ID  = aws_bedrockagent_knowledge_base.kb_v2.id
    }
  }
}
