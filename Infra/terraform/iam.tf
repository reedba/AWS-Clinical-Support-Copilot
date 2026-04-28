# Lookup account and caller identity for dynamic IAM principals.
data "aws_caller_identity" "current" {}

locals {
  current_arn       = data.aws_caller_identity.current.arn
  current_user_name = can(regex(":user/", local.current_arn)) ? element(split("/", local.current_arn), 1) : null
}

# Allow the current IAM user (when using user credentials) to assume the KB role
# for local index bootstrap operations.
resource "aws_iam_policy" "kb_role_assume_for_bootstrap" {
  name = "kb-role-assume-for-bootstrap"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["sts:AssumeRole"]
        Resource = [aws_iam_role.bedrock_kb_v2.arn]
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "kb_role_assume_for_bootstrap" {
  count      = local.current_user_name == null ? 0 : 1
  user       = local.current_user_name
  policy_arn = aws_iam_policy.kb_role_assume_for_bootstrap.arn
}

# IAM role Bedrock assumes for Knowledge Base indexing and ingestion.
resource "aws_iam_role" "bedrock_kb_v2" {
  name = "bedrock-kb-v2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "bedrock.amazonaws.com" }
        Action    = "sts:AssumeRole"
      },
      {
        Effect    = "Allow"
        Principal = { AWS = local.current_arn }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "bedrock_kb_v2" {
  name = "bedrock-kb-v2-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          aws_s3_bucket.docs_v2.arn,
          "${aws_s3_bucket.docs_v2.arn}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["aoss:APIAccessAll"]
        Resource = ["*"]
      },
      {
        Effect = "Allow"
        Action = [
          "aoss:CreateIndex",
          "aoss:DeleteIndex",
          "aoss:UpdateIndex",
          "aoss:DescribeIndex",
          "aoss:ReadDocument",
          "aoss:WriteDocument",
        ]
        Resource = ["*"]
      },
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = [
          "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bedrock_kb_v2" {
  role       = aws_iam_role.bedrock_kb_v2.name
  policy_arn = aws_iam_policy.bedrock_kb_v2.arn
}
