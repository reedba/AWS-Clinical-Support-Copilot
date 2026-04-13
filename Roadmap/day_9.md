
# Day 9: Priorities & Checklist

## Priorities
- Add prompt rules and structured templates for outputs
- Ensure outputs are clean, consistent, and operations-focused
- Improve control over AI responses for different use cases

## Checklist

- [ ] Create prompt templates for:
	- [ ] Policy Q&A
	- [ ] Intake summarization
	- [ ] Administrative action drafting
	- [ ] Escalation routing
- [ ] Implement structured output formats, e.g.:
	```json
	{
		"patient_intake_summary": {
			"visit_reason": "Follow-up appointment request",
			"reported_non_clinical_concerns": ["needs scheduling", "insurance verification pending"],
			"recommended_admin_next_step": "Route to scheduling and insurance verification queue",
			"requires_human_review": true
		}
	}
	```
- [ ] Test outputs for clarity and structure
- [ ] Document prompt templates and output formats

---

**Deliverable:**
Cleaner, more controlled outputs using prompt rules and structured templates for all major use cases.
