terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.5"
    }
  }

  # Uncomment and configure this backend when you are ready to store state remotely.
  # backend "s3" {
  #   bucket         = "your-terraform-state-bucket"
  #   key            = "clinical-support/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "your-terraform-lock-table"
  #   encrypt        = true
  # }
}
