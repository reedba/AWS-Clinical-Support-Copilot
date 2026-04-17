
# Day 6: Priorities & Checklist

## Priorities
- Build the Gradio UI for chat and intake
- Integrate Gradio frontend with API Gateway backend
- Keep the UI simple and focused on core features

## Checklist

- [x] Set up Gradio project in `frontend/`
- [x] Implement chat box for user questions
- [x] Connect Gradio to API Gateway /chat endpoint
- [x] Display response output and source documents (if available)
- [x] Test end-to-end flow from UI to backend
- [x] Keep styling minimal (focus on function)

## Notes

- Issue: PowerShell alias for curl does not support -X/-H/-d. Fix: use Invoke-RestMethod or curl.exe.
- Issue: Gradio v6 Chatbot expects message dicts. Fix: return [{'role': 'user', 'content': ...}, {'role': 'assistant', 'content': ...}].
- Issue: Global pip conflicts with gradio versions. Fix: create a local .venv and install frontend/requirements.txt.
- Issue: Bedrock InvokeModel AccessDenied. Fix: add bedrock:InvokeModel permission to the Lambda role.

## Test Questions (Gradio UI)

- What forms are required for a new patient intake?
- Summarize the new patient intake process for front desk staff.
- What is the callback escalation procedure if a patient misses a follow-up?
- What is the discharge follow-up checklist?
- How should we handle a referral coordination request?
- What does the prior authorization workflow require?

---

**Deliverable:**
End-to-end UI talking to AWS backend, supporting chat and displaying grounded responses.
