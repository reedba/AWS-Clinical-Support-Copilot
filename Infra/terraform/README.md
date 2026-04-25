# Terraform (AWS)

Minimal Terraform scaffold using the AWS provider and the default CLI profile.

## Quick start

```bash
terraform init
terraform plan
```

## Notes

- This configuration uses the AWS CLI profile `default` and region `us-east-1`.
- To use a remote backend later, uncomment and fill in the `backend "s3"` block in `versions.tf`.
