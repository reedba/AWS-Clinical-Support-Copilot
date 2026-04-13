# AI Clinical Support Copilot (HIPAA-Aware Architecture)

## What is this project?

**AI Clinical Support Copilot** is a regulated-industry-ready, AWS-native assistant for healthcare operations teams. It is designed to help staff answer policy questions, summarize intake information, and safely route sensitive administrative actions through approval workflows. The architecture is HIPAA-aware, prioritizing privacy, auditability, and security.

---

## What it does

A healthcare staff member can:

- Ask questions about clinic policies and procedures
- Get grounded answers from approved internal documents
- Create intake summaries from structured patient input
- Draft administrative follow-up actions
- Send sensitive actions into an approval workflow

## What it does **not** do

- Diagnose patients
- Recommend treatment
- Replace clinicians
- Act on PHI with no controls

> **Disclaimer:** This project is a HIPAA-aware educational architecture prototype and is not a production-certified healthcare system.

---

## Core Use Case

Build a clinical operations assistant for:

- Front desk staff
- Operations staff
- Care coordinators
- Intake/admin teams

### Example Supported Tasks

- “What forms are required for a new patient intake?”
- “Summarize this intake note for staff review.”
- “What is the follow-up process after discharge?”
- “Draft a callback request for this patient.”
- “Start a prior-authorization follow-up request.”

---

## Architecture Overview

### Frontend
- Gradio (for rapid prototyping and UI)

### Backend
- API Gateway (REST endpoint)
- Lambda (chat and workflow orchestration)

### AI Layer
- Amazon Bedrock (LLM)
- Bedrock Knowledge Base (RAG over policy docs)
- Bedrock Guardrails (domain constraints)

### Data/Storage
- S3 (policy/procedure documents)
- DynamoDB (sessions, intake summaries, workflow state)

### Workflow
- Step Functions (approval/review flow)

### Observability/Security
- CloudWatch (logging, monitoring)
- IAM (least-privilege access)

---

## 2-Week Build Plan

### Week 1: Build the MVP
1. Define use case, repo structure, and architecture
2. Prepare realistic healthcare documents and sample data (fake only)
3. Set up S3 + Bedrock Knowledge Base
4. Build Lambda for chat and retrieval orchestration
5. Add API Gateway endpoint
6. Build Gradio UI
7. Add DynamoDB for sessions and intake summaries

**Milestone:** End-to-end MVP with Gradio frontend, API Gateway, Lambda backend, Bedrock Knowledge Base, S3, and DynamoDB.

### Week 2: Regulated-Industry Features
8. Add Bedrock Guardrails (no diagnosis/treatment, admin-only)
9. Add prompt rules and structured templates
10. Add Step Functions approval workflow
11. Add CloudWatch logging and error handling
12. Add HIPAA-aware design decisions and documentation
13. Polish README, add architecture diagram, screenshots, and rationale
14. Record demo video and create LinkedIn content

---

## Why this matters in healthcare

- Reduces staff burnout and admin overload
- Provides consistent, policy-grounded answers
- Improves workflow efficiency and auditability
- Demonstrates realistic, privacy-conscious AI in a regulated setting

---

## Why I chose these AWS services

- **Bedrock:** Managed foundation model access
- **Knowledge Base:** RAG over policy documents
- **Guardrails:** Domain constraints and safety
- **Lambda:** Serverless orchestration
- **API Gateway:** Clean external API
- **DynamoDB:** Session/workflow state
- **Step Functions:** Approval flows
- **CloudWatch:** Auditability and debugging
- **S3:** Document storage

---

## Security Considerations

- Least-privilege IAM roles
- Avoid unnecessary PHI storage
- Use only fake data for demo
- Log metadata, not sensitive content
- Human review for sensitive workflows

---

## Future Improvements

- React frontend
- Django backend/service layer
- Cognito authentication
- Role-based dashboards
- More workflow integrations

---

## Demo & Screenshots

_Add screenshots and a link to your demo video here._

---

## Disclaimer

This project is a HIPAA-aware educational architecture prototype and is not a production-certified healthcare system. No real patient data is used. For demonstration purposes only.
