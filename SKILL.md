---
name: aws-clinical-support-copilot
description: Enforces daily roadmap discipline and project best practices for the AWS Clinical Support Copilot.
---

# Workflow Skill: Guided Roadmap Execution

## Purpose
This skill enforces a disciplined, day-by-day build process using the Roadmap checklists. The agent (and team) must not proceed to the next day's tasks until all checklist items for the current day are completed.

## Rules

## How to Use

# SKILL: AWS Clinical Support Copilot Project Patterns

## Purpose
This skill file defines best practices, conventions, and reusable patterns for building and maintaining the AI Clinical Support Copilot project. It is intended to ensure consistency, security, and regulated-industry readiness throughout the codebase.
---

- Use a `Roadmap/` folder for day-by-day build plans and checklists.
---

- Add clear disclaimers in README and UI: "HIPAA-aware prototype, not production-certified."
---

- Always return structured JSON responses from Lambda for downstream processing.
---

- Log all major events and errors to CloudWatch.
---

- Do not expose any PHI or sensitive data in the UI.
---

- Use Markdown checklists for daily priorities and progress tracking in `Roadmap/`.

---
- Ensure audit trails are in place for all sensitive actions.

---
- Follow the patterns and checklists to ensure regulated-industry readiness and project consistency.
- Update this file as new best practices emerge during the project.
