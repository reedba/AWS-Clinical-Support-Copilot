# Terraform resources are split by concern for easier maintenance:
# - s3.tf         : S3 bucket and hardening
# - iam.tf        : shared identity and Bedrock KB IAM role/policies
# - bedrock_kb.tf : AOSS collection/policies, KB, and data source
# - lambda.tf     : Lambda package + function + Lambda IAM