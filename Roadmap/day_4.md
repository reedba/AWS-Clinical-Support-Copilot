
# Day 4: Priorities & Checklist

## Priorities
- Build the first Lambda for chat and retrieval orchestration
- Integrate Lambda with Bedrock Knowledge Base
- Design structured response formats for policy answers and admin summaries

## Checklist

- [ ] Create Lambda function for:
	- [ ] Receiving user prompts
	- [ ] Calling Bedrock/Knowledge Base
	- [ ] Returning grounded responses
	- [ ] Tagging request type (policy answer, admin summary)
- [ ] Support two response modes:
	- [ ] Policy/procedure answer
	- [ ] Structured admin summary
- [ ] Return structured JSON responses, e.g.:
	```json
	{
		"response_type": "policy_answer",
		"answer": "Patients must complete...",
		"sources": ["patient_intake_policy.pdf"],
		"confidence_note": "Grounded in internal policy documents."
	}
	```
- [ ] Test Lambda with sample prompts and validate outputs

---

**Deliverable:**
A working Lambda that talks to Bedrock and returns useful, structured output for policy and admin queries.
