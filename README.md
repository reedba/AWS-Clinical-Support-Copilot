
# AI Clinical Support Copilot (HIPAA-Aware Architecture)

## Project Overview

The AI Clinical Support Copilot is designed to streamline healthcare operations by providing staff with an intelligent assistant that answers policy questions, summarizes intake information, and routes administrative actions through secure approval workflows. Built with AWS-native services and a HIPAA-aware architecture, the project demonstrates how AI can be safely integrated into regulated healthcare environments to improve efficiency, consistency, and auditability.

## Problem Statement

Healthcare operations teams face increasing administrative burdens, from answering complex policy questions to managing intake and routing sensitive actions for approval. Manual processes are time-consuming, error-prone, and can lead to inconsistent outcomes. There is a need for a secure, privacy-conscious assistant that can provide grounded answers, automate routine tasks, and ensure sensitive actions are handled with proper oversight—without risking patient privacy or regulatory compliance.

## Architecture Notes

- The solution uses AWS services to ensure scalability, security, and compliance.
- Gradio provides a rapid prototyping frontend for staff interaction.
- API Gateway and Lambda orchestrate chat, retrieval, and workflow logic.
- Amazon Bedrock powers the AI layer, with Knowledge Base for RAG over policy documents and Guardrails for domain constraints.
- S3 stores policy and procedure documents; DynamoDB manages session and workflow state.
- Step Functions handle approval workflows, ensuring human-in-the-loop for sensitive actions.
- CloudWatch and IAM provide observability and least-privilege security.
- The architecture is designed to avoid unnecessary PHI storage and to log only metadata, supporting HIPAA principles.

---


## What it does

- Answers clinic policy and procedure questions
- Provides grounded responses from approved internal documents
- Summarizes intake information from structured input
- Drafts administrative follow-up actions
- Routes sensitive actions into an approval workflow

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

**Example Supported Tasks:**
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
### Architecture Diagram

```mermaid
flowchart TD
	A[Gradio Frontend] -->|REST API| B[API Gateway]
	B --> C[Lambda Backend]
	C -->|RAG Query| D[Bedrock Knowledge Base]
	D -->|Docs| E[S3: Policy/Procedure Docs]
	C -->|Guardrails| F[Bedrock Guardrails]
	C -->|Session/Workflow State| G[DynamoDB]
	C -->|Approval Workflow| H[Step Functions]
	H --> G
	C -->|Logs| I[CloudWatch]
	C -->|IAM Roles| J[IAM]
	subgraph AWS Cloud
		B
		C
		D
		E
		F
		G
		H
		I
		J
	end
```
