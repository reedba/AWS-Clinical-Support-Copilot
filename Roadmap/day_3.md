
# Day 3: Priorities & Checklist

## Priorities
- Set up S3 bucket for healthcare documents
- Configure Bedrock Knowledge Base and connect to S3
- Test knowledge retrieval against sample documents

## Checklist

- [ ] Create S3 bucket for healthcare documents
- [ ] Upload sample documents from `samples/` to S3
- [ ] Configure Bedrock Knowledge Base
- [ ] Connect Knowledge Base to S3 bucket
- [ ] Test retrieval with sample queries:
	- [ ] “What documents are required for a new patient?”
	- [ ] “What is the callback escalation workflow?”
	- [ ] “What should staff do after discharge follow-up is missed?”
- [ ] Validate that answers are grounded in uploaded documents

---

**Deliverable:**
Knowledge retrieval working against your healthcare documents in S3 via Bedrock Knowledge Base.
