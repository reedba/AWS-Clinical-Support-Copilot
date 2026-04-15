
# Day 3: Priorities & Checklist

## Priorities
- Set up S3 bucket for healthcare documents
- Configure Bedrock Knowledge Base and connect to S3
- Test knowledge retrieval against sample documents

## Checklist

- [x] Create S3 bucket for healthcare documents
- [x] Upload sample documents from `samples/` to S3
- [x] Configure Bedrock Knowledge Base
- [x] Connect Knowledge Base to S3 bucket
- [x] Test retrieval with sample queries:
	- [x] “What documents are required for a new patient?”
	- [x] “What is the callback escalation workflow?”
	- [x] “What should staff do after discharge follow-up is missed?”
- [x] Validate that answers are grounded in uploaded documents

## S3 Bucket Setup

1. Create a bucket in the AWS Console or with AWS CLI.
2. Choose a globally unique bucket name and the same region as your Lambda/Bedrock resources.
3. Block all public access.
4. Enable default encryption (SSE-S3 or SSE-KMS).
5. Optionally enable versioning for audit/history.
6. Grant access only to the IAM role used by your Lambda and Bedrock Knowledge Base.
   - Create an IAM role for your Lambda function (covered in later days).
   - Attach this policy to the role, replacing `your-bucket-name` with your actual bucket:
     ```json
     {
         "Version": "2012-10-17",
         "Statement": [
             {
                 "Effect": "Allow",
                 "Action": [
                     "s3:GetObject",
                     "s3:ListBucket"
                 ],
                 "Resource": [
                     "arn:aws:s3:::your-bucket-name",
                     "arn:aws:s3:::your-bucket-name/*"
                 ]
             }
         ]
     }
     ```
   - For Bedrock Knowledge Base, ensure the role has `bedrock:Retrieve` permissions on the knowledge base.
7. Upload the sample documents from `Samples/` into the bucket.
   ```powershell
   aws s3 cp .\Samples\ s3://my-hipaa-copilot-docs-brandonreed-2026 --recursive
   ```
   Verify upload:
   ```powershell
   aws s3 ls s3://my-hipaa-copilot-docs-brandonreed-2026 --recursive
   ```
8. Record the bucket name for Knowledge Base configuration.

> Optional versioning command:
> ```powershell
> aws s3api put-bucket-versioning \
>   --bucket my-hipaa-copilot-docs-brandonreed-2026 \
>   --versioning-configuration Status=Enabled
> ```
> 
> Verify versioning:
> ```powershell
> aws s3api get-bucket-versioning --bucket my-hipaa-copilot-docs-brandonreed-2026
> ```
> Expected output:
> ```json
> {
>     "Status": "Enabled"
> }
> ```



> CLI example:
> ```powershell
> aws s3api create-bucket \
>   --bucket my-hipaa-copilot-docs-brandonreed-2026 \
>   --region us-east-1
> 
> aws s3api put-public-access-block \
>   --bucket my-hipaa-copilot-docs-brandonreed-2026 \
>   --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
> 
> aws s3api get-public-access-block \
>   --bucket my-hipaa-copilot-docs-brandonreed-2026
> 
> aws s3api put-bucket-encryption \
>   --bucket my-hipaa-copilot-docs-brandonreed-2026 \
>   --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
> 
> aws s3api get-bucket-encryption \
>   --bucket my-hipaa-copilot-docs-brandonreed-2026
> ```
> 
> Expected output from `get-public-access-block`:
> ```json
> {
>     "PublicAccessBlockConfiguration": {
>         "BlockPublicAcls": true,
>         "IgnorePublicAcls": true,
>         "BlockPublicPolicy": true,
>         "RestrictPublicBuckets": true
>     }
> }
> ```
> 
> Expected output from `get-bucket-encryption`:
> ```json
> {
>     "ServerSideEncryptionConfiguration": {
>         "Rules": [
>             {
>                 "ApplyServerSideEncryptionByDefault": {
>                     "SSEAlgorithm": "AES256"
>                 },
>                 "BucketKeyEnabled": false,
>                 "BlockedEncryptionTypes": {
>                     "EncryptionType": [
>                         "SSE-C"
>                     ]
>                 }
>             }
>         ]
>     }
> }
> ```




---

**Deliverable:**
Knowledge retrieval working against your healthcare documents in S3 via Bedrock Knowledge Base.
