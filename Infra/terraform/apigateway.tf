# ===== API GATEWAY (HTTP API) → bedrock-retrieval-lambda-v2 =====
#
# Uses API Gateway v2 (HTTP API) — cheaper and lower-latency than REST API.
# Single route: POST /chat → Lambda proxy integration.

resource "aws_apigatewayv2_api" "copilot" {
  name          = "clinical-support-copilot-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["Content-Type"]
    max_age       = 300
  }
}

resource "aws_apigatewayv2_integration" "copilot_lambda" {
  api_id                 = aws_apigatewayv2_api.copilot.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.bedrock_lambda_v2.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "copilot_chat" {
  api_id    = aws_apigatewayv2_api.copilot.id
  route_key = "POST /chat"
  target    = "integrations/${aws_apigatewayv2_integration.copilot_lambda.id}"
}

resource "aws_apigatewayv2_stage" "copilot_dev" {
  api_id      = aws_apigatewayv2_api.copilot.id
  name        = "dev"
  auto_deploy = true
}

# Allow API Gateway to invoke the Lambda function.
resource "aws_lambda_permission" "apigw_copilot" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.bedrock_lambda_v2.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.copilot.execution_arn}/*/*"
}

output "api_base_url" {
  description = "Set this as API_BASE_URL in the Gradio frontend."
  value       = aws_apigatewayv2_stage.copilot_dev.invoke_url
}
