# S3 bucket for v2 policy documents used by Bedrock Knowledge Base.
resource "aws_s3_bucket" "docs_v2" {
  bucket = "my-hipaa-copilot-docs-brandonreed-2026-v2"
}

# Block all forms of public access for this bucket.
resource "aws_s3_bucket_public_access_block" "docs_v2" {
  bucket                  = aws_s3_bucket.docs_v2.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# Enable versioning to protect against accidental deletes/overwrites.
resource "aws_s3_bucket_versioning" "docs_v2" {
  bucket = aws_s3_bucket.docs_v2.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Enforce default SSE-S3 encryption for objects.
resource "aws_s3_bucket_server_side_encryption_configuration" "docs_v2" {
  bucket = aws_s3_bucket.docs_v2.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
