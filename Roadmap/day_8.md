
# Day 8: Priorities & Checklist

## Priorities
- Add Bedrock Guardrails to restrict unsafe or out-of-scope responses
- Ensure the system only provides administrative and policy guidance
- Prevent diagnosis, treatment recommendations, or inappropriate content

## Checklist

- [ ] Define guardrail rules:
	- [ ] Only provide administrative/policy guidance
	- [ ] Do not provide medical advice or diagnosis
	- [ ] Escalate clinical questions to licensed staff
	- [ ] Avoid revealing unnecessary sensitive details
- [ ] Implement Bedrock Guardrails in the AI layer
- [ ] Add fallback responses for restricted queries, e.g.:
	> “I can help with administrative and policy-related support, but I cannot provide diagnosis or treatment recommendations. Please escalate clinical questions to licensed staff.”
- [ ] Test guardrails with restricted and allowed prompts
- [ ] Document guardrail logic and fallback behavior

---

**Deliverable:**
Safe, bounded system behavior with clear restrictions and fallback responses enforced by Bedrock Guardrails.
