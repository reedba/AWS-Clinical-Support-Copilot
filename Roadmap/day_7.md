
# Day 7: Priorities & Checklist

## Priorities
- Add DynamoDB for session and intake summary storage
- Ensure all prompts, responses, and actions are saved for auditability
- Support stateful and reviewable workflows

## Checklist

- [ ] Add optional intake form tab (moved from Day 6)
- [ ] Create DynamoDB tables (or one-table design) for:
	- [ ] Sessions
	- [ ] Intake summaries
	- [ ] Workflow state
- [ ] Store the following for each session:
	- [ ] session_id
	- [ ] timestamp
	- [ ] user_role
	- [ ] input_text
	- [ ] output_text
	- [ ] action_type
	- [ ] status
- [ ] For intake summaries, also store:
	- [ ] intake_id
	- [ ] structured_summary
	- [ ] review_status
- [ ] Save every prompt/response and generated intake summary
- [ ] Save pending action requests
- [ ] Test data persistence and retrieval

---

**Deliverable:**
System is now stateful and auditable with DynamoDB storing sessions, summaries, and workflow state.
