# ===== OPENSEARCH SERVERLESS (vector store for Bedrock KB) =====

# Encryption policy — required before the AOSS collection can be created.
resource "aws_opensearchserverless_security_policy" "kb_v2_encryption" {
  name = "kb-v2-encryption"
  type = "encryption"

  policy = jsonencode({
    Rules = [
      {
        ResourceType = "collection"
        Resource     = ["collection/kb-v2"]
      }
    ]
    AWSOwnedKey = true
  })
}

# Network policy — allows Bedrock (an AWS service) to reach the collection.
resource "aws_opensearchserverless_security_policy" "kb_v2_network" {
  name = "kb-v2-network"
  type = "network"

  policy = jsonencode([
    {
      Rules = [
        {
          ResourceType = "collection"
          Resource     = ["collection/kb-v2"]
        }
      ]
      AllowFromPublic = true
    }
  ])
}

# The AOSS collection that stores document embeddings.
resource "aws_opensearchserverless_collection" "kb_v2" {
  name = "kb-v2"
  type = "VECTORSEARCH"

  depends_on = [
    aws_opensearchserverless_security_policy.kb_v2_encryption,
    aws_opensearchserverless_security_policy.kb_v2_network,
  ]
}

# Access policy — grants the Bedrock KB role read/write access to collection and index.
resource "aws_opensearchserverless_access_policy" "kb_v2" {
  name = "kb-v2-access"
  type = "data"

  depends_on = [aws_iam_role.bedrock_kb_v2]

  policy = jsonencode([
    {
      Rules = [
        {
          ResourceType = "collection"
          Resource     = ["collection/kb-v2"]
          Permission = [
            "aoss:CreateCollectionItems",
            "aoss:DeleteCollectionItems",
            "aoss:UpdateCollectionItems",
            "aoss:DescribeCollectionItems",
          ]
        },
        {
          ResourceType = "index"
          Resource     = ["index/kb-v2/*"]
          Permission = [
            "aoss:CreateIndex",
            "aoss:DeleteIndex",
            "aoss:UpdateIndex",
            "aoss:DescribeIndex",
            "aoss:ReadDocument",
            "aoss:WriteDocument",
          ]
        }
      ]
      Principal = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/bedrock-kb-v2-role",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root",
        local.current_arn,
      ]
    }
  ])
}

# Pre-create vector index before KB creation. Bedrock requires index existence.
resource "null_resource" "kb_v2_index" {
  triggers = {
    collection_id = aws_opensearchserverless_collection.kb_v2.id
    endpoint      = aws_opensearchserverless_collection.kb_v2.collection_endpoint
  }

  depends_on = [
    aws_opensearchserverless_collection.kb_v2,
    aws_opensearchserverless_access_policy.kb_v2,
    aws_iam_user_policy_attachment.kb_role_assume_for_bootstrap,
    aws_iam_role.bedrock_kb_v2,
    aws_iam_role_policy_attachment.bedrock_kb_v2,
  ]

  provisioner "local-exec" {
    interpreter = ["PowerShell", "-Command"]
    command     = "& '${path.module}/../../.venv/Scripts/python.exe' '${path.module}/../../scripts/create_aoss_index.py'"
    environment = {
      COLLECTION_ENDPOINT = aws_opensearchserverless_collection.kb_v2.collection_endpoint
      INDEX_NAME          = "kb-v2-index"
      REGION              = "us-east-1"
    }
  }
}

# ===== BEDROCK KNOWLEDGE BASE =====

resource "aws_bedrockagent_knowledge_base" "kb_v2" {
  name     = "clinical-support-kb-v2"
  role_arn = aws_iam_role.bedrock_kb_v2.arn

  knowledge_base_configuration {
    type = "VECTOR"
    vector_knowledge_base_configuration {
      embedding_model_arn = "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0"
    }
  }

  storage_configuration {
    type = "OPENSEARCH_SERVERLESS"
    opensearch_serverless_configuration {
      collection_arn    = aws_opensearchserverless_collection.kb_v2.arn
      vector_index_name = "kb-v2-index"
      field_mapping {
        vector_field   = "vector"
        text_field     = "text"
        metadata_field = "metadata"
      }
    }
  }

  depends_on = [
    aws_opensearchserverless_access_policy.kb_v2,
    aws_iam_role_policy_attachment.bedrock_kb_v2,
    null_resource.kb_v2_index,
  ]
}

# Data source pointing to the whole v2 bucket.
resource "aws_bedrockagent_data_source" "kb_v2_s3" {
  name              = "clinical-support-kb-v2-s3"
  knowledge_base_id = aws_bedrockagent_knowledge_base.kb_v2.id

  data_source_configuration {
    type = "S3"
    s3_configuration {
      bucket_arn = aws_s3_bucket.docs_v2.arn
    }
  }
}
