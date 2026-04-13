
# Day 10: Priorities & Checklist

## Priorities
- Add Step Functions for approval and review workflows
- Integrate Lambda with Step Functions for sensitive administrative actions
- Simulate reviewer approval/rejection for demo purposes

## Checklist

- [ ] Define use cases for approval workflows (e.g., callback case, access change, follow-up escalation, prior-auth follow-up, patient contact task)
- [ ] Update Lambda to classify and trigger approval-required actions
- [ ] Create Step Functions workflow for approval/review
- [ ] Store pending items in DynamoDB
- [ ] Simulate reviewer approval/rejection (API endpoint, manual script, or Gradio admin view)
- [ ] Update workflow status in DynamoDB
- [ ] Test end-to-end approval flow
- [ ] Document workflow logic and demo steps

---

**Deliverable:**
Real workflow orchestration for sensitive actions, with approval/review flow managed by Step Functions and DynamoDB.
