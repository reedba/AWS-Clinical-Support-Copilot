
# Day 5: Priorities & Checklist

## Priorities
- Put API Gateway in front of Lambda
- Create and test the /chat endpoint
- Ensure stable request/response format for integration

## Checklist

- [ ] Create /chat endpoint in API Gateway
- [ ] Connect API Gateway to Lambda function
- [ ] Test endpoint with Postman or curl
- [ ] Validate request/response format, e.g.:
	```json
	{
		"session_id": "abc123",
		"user_role": "front_desk_staff",
		"message": "What forms are required for new patient intake?"
	}
	```
- [ ] Confirm Lambda returns structured response
- [ ] Document the API contract (input/output)

---

**Deliverable:**
Stable backend API endpoint for chat, ready for frontend integration.
