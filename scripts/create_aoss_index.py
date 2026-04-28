"""
Creates the knn vector index in an OpenSearch Serverless (AOSS) collection
that Bedrock Knowledge Base requires before it can be provisioned.

Bedrock does NOT create the index itself — it expects the index to already
exist with the correct field mappings (vector, text, metadata).

Usage (called by Terraform null_resource local-exec):
  python scripts/create_aoss_index.py

Required env vars (set by Terraform):
  COLLECTION_ENDPOINT  - Full HTTPS endpoint of the AOSS collection
  INDEX_NAME           - Name of the index to create (e.g. kb-v2-index)
  REGION               - AWS region (e.g. us-east-1)
"""

import boto3
import os
import sys
import time
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

# ===== CONFIG FROM ENV =====
region   = os.environ["REGION"]
endpoint = os.environ["COLLECTION_ENDPOINT"].rstrip("/")
index    = os.environ["INDEX_NAME"]

# Strip protocol — opensearch-py takes just the hostname
host = endpoint.replace("https://", "").replace("http://", "")

# ===== AUTH =====
# Use the caller's own credentials directly.
# The AOSS data access policy includes the IAM user as a principal.
session     = boto3.Session()
credentials = session.get_credentials()

caller = boto3.client("sts", region_name=region).get_caller_identity()
print(f"Signing as: {caller.get('Arn')}")

auth = AWSV4SignerAuth(credentials, region, "aoss")

client = OpenSearch(
    hosts=[{"host": host, "port": 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    pool_maxsize=20,
    timeout=30,
)

# ===== INDEX BODY =====
# Titan Embed Text v2 produces 1024-dimensional vectors.
# Field names (vector, text, metadata) must match the Terraform field_mapping.
index_body = {
    "settings": {
        "index.knn": True
    },
    "mappings": {
        "properties": {
            "vector": {
                "type": "knn_vector",
                "dimension": 1024,
                "method": {
                    "name": "hnsw",
                    "engine": "faiss"
                }
            },
            "text":     {"type": "text"},
            "metadata": {"type": "text"}
        }
    }
}

print(f"Creating index '{index}' in {endpoint} ...")

# AOSS policy/permission updates can take a short time to propagate after apply.
for attempt in range(1, 19):
    try:
        if client.indices.exists(index=index):
            print(f"Index '{index}' already exists — skipping creation.")
            sys.exit(0)

        response = client.indices.create(index=index, body=index_body)
        print(f"Attempt {attempt}: {response}")
        print("Index created successfully.")
        sys.exit(0)

    except Exception as e:
        err = str(e)
        print(f"Attempt {attempt}: {err}")

        # resource_already_exists_exception — treat as success
        if "resource_already_exists_exception" in err.lower():
            print("Index already exists — proceeding.")
            sys.exit(0)

        # 403 — policy may not have propagated yet, retry
        if "403" in err:
            time.sleep(10)
            continue

        # Non-retryable error
        break

print("ERROR: index creation failed.")
sys.exit(1)
