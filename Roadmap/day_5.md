
# Day 5: Priorities & Checklist

## Priorities
- Put API Gateway in front of Lambda
- Create and test the /chat endpoint
- Ensure stable request/response format for integration

## Checklist

- [x] Create /chat endpoint in API Gateway
- [x] Connect API Gateway to Lambda function
- [x] Test endpoint with Postman or curl
- [x] Validate request/response format, e.g.:
	```json
	{
		"session_id": "abc123",
		"user_role": "front_desk_staff",
		"message": "What forms are required for new patient intake?"
	}
	```
- [x] Confirm Lambda returns structured response
- [x] Document the API contract (input/output)

## Notes

- Invoke URL: https://ymoxmockwe.execute-api.us-east-1.amazonaws.com/dev
- Why: HTTP API Gateway sits in front of Lambda to provide a stable /chat endpoint for the frontend.
- What we did: created an HTTP API, added POST /chat, integrated Lambda, and deployed to stage dev.
- Test command (curl.exe):
	```bash
	curl -X POST "https://ymoxmockwe.execute-api.us-east-1.amazonaws.com/dev/chat" \
	  -H "Content-Type: application/json" \
	  -d '{"prompt":"What forms are required for new patient intake?","request_type":"policy_answer"}'
	```
- Test command (PowerShell Invoke-RestMethod):
	```powershell
	Invoke-RestMethod -Method Post `
	  -Uri "https://ymoxmockwe.execute-api.us-east-1.amazonaws.com/dev/chat" `
	  -ContentType "application/json" `
	  -Body '{"prompt":"What forms are required for new patient intake?","request_type":"policy_answer"}'
	```

## API Contract

**Endpoint**

- Method: POST
- Path: /chat
- Content-Type: application/json

**Request Body**

```json
{
	"prompt": "What forms are required for new patient intake?",
	"request_type": "policy_answer"
}
```

**Request Fields**

- prompt (string, required): User question or prompt.
- request_type (string, optional): "policy_answer" (default) or "admin_summary".

**Success Response (200)**

```json
{
	"response_type": "policy_answer",
	"answer": "...",
	"sources": ["..."],
	"confidence_note": "Grounded in internal policy documents."
}
```

**Alternate Response (admin_summary)**

```json
{
	"response_type": "admin_summary",
	"summary": "...",
	"sources": ["..."],
	"confidence_note": "Grounded in internal policy documents."
}
```

**Error Responses**

- 400: {"error": "prompt is required"}
- 500: {"error": "Internal server error", "details": "..."}

---

**Deliverable:**
Stable backend API endpoint for chat, ready for frontend integration.
