
name: aws-clinical-support-copilot

# Workflow Skill: Guided Roadmap Execution

## Purpose
This skill enforces a disciplined, day-by-day build process using the Roadmap checklists. The agent (and team) must not proceed to the next day's tasks until all checklist items for the current day are completed.

## Rules
- Each day in `Roadmap/` (e.g., `day_1.md`, `day_2.md`, ...) contains a checklist of tasks.
- Work must be performed in ascending numerical order (Day 1, Day 2, ...).
- Do not begin any checklist item for Day N+1 until all items for Day N are checked off as completed.
- If a checklist item is blocked, document the blocker in the file and pause further progress until resolved.
- Mark each completed checklist item with `[x]` in the Markdown file.
- Only after all items for a day are marked complete, move to the next day's file.
- At the start of each day, review the checklist and priorities before beginning work.

## How to Use
- Use this skill to guide daily standups, development, and reviews.
- The agent should enforce this workflow when automating or assisting with project tasks.
- Update this section if the roadmap process changes.
name: aws-clinical-support-copilot

# SKILL: AWS Clinical Support Copilot Project Patterns

## Purpose
This skill file defines best practices, conventions, and reusable patterns for building and maintaining the AI Clinical Support Copilot project. It is intended to ensure consistency, security, and regulated-industry readiness throughout the codebase.

---

## Project Structure
- Use clear, purpose-driven folders: `frontend/`, `lambdas/`, `infra/`, `docs/`, `prompts/`, `samples/`, `Roadmap/`.
- Place all sample data and documents in `samples/`.
- Store all architecture, design, and process documentation in `docs/`.
- Use a `Roadmap/` folder for day-by-day build plans and checklists.

---

## Security & Compliance
- Always use least-privilege IAM roles for all AWS resources.
- Never store real PHI; use only fake/demo data for development and testing.
- Log only metadata, not sensitive content.
- Ensure all sensitive workflows require human review and approval.
- Add clear disclaimers in README and UI: "HIPAA-aware prototype, not production-certified."

---

## AI/Bedrock Integration
- Use Bedrock Knowledge Base for RAG over policy/procedure documents.
- Implement Bedrock Guardrails to restrict medical advice, diagnosis, or inappropriate content.
- Use structured prompt templates for each use case (policy Q&A, intake summary, admin actions).
- Always return structured JSON responses from Lambda for downstream processing.

---

## API & Backend
- All external API access should go through API Gateway.
- Lambda functions must validate input and handle errors gracefully.
- Use DynamoDB for session, intake summary, and workflow state storage.
- Integrate Step Functions for approval/review workflows.
- Log all major events and errors to CloudWatch.

---

## Frontend
- Use Gradio for rapid prototyping and demonstration.
- Keep UI simple and focused on core workflow tasks.
- Display source documents and confidence notes when available.
- Do not expose any PHI or sensitive data in the UI.

---

## Documentation & Roadmap
- Maintain a detailed README with architecture diagram, rationale, and security considerations.
- Use Markdown checklists for daily priorities and progress tracking in `Roadmap/`.
- Document all prompt templates, API contracts, and workflow logic in `docs/`.

---

## Review & Audit
- Regularly review code and documentation for privacy and security risks.
- Ensure audit trails are in place for all sensitive actions.
- Highlight human review and approval steps in all workflow documentation.

---

## How to Use This Skill
- Reference this SKILL.md before adding new features or making architectural changes.
- Follow the patterns and checklists to ensure regulated-industry readiness and project consistency.
- Update this file as new best practices emerge during the project.
