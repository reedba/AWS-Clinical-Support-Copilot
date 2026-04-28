import os
from typing import Dict, List, Tuple

import gradio as gr
import requests


API_BASE_URL = os.getenv(
	"API_BASE_URL",
	"https://t6grjk401i.execute-api.us-east-1.amazonaws.com/dev",
)
CHAT_URL = f"{API_BASE_URL.rstrip('/')}/chat"


def call_chat_api(prompt: str, request_type: str) -> dict:
	# Keep a small timeout to avoid hanging the UI if the backend is slow.
	response = requests.post(
		CHAT_URL,
		json={"prompt": prompt, "request_type": request_type},
		timeout=20,
	)
	response.raise_for_status()
	return response.json()


def format_response(payload: dict) -> str:
	response_type = payload.get("response_type", "policy_answer")
	if response_type == "admin_summary":
		main_text = payload.get("summary", "")
	else:
		main_text = payload.get("answer", "")
	sources = payload.get("sources", [])
	confidence = payload.get("confidence_note", "")

	lines = [main_text.strip()]
	if sources:
		lines.append("\nSources: " + ", ".join(sources))
	if confidence:
		lines.append("\n" + confidence)
	return "\n".join([line for line in lines if line])


def handle_chat(
	user_message: str,
	request_type: str,
	history: List[Dict[str, str]],
) -> Tuple[List[Dict[str, str]], str]:
	if not user_message.strip():
		return history, ""

	try:
		payload = call_chat_api(user_message.strip(), request_type)
		assistant_reply = format_response(payload)
	except requests.RequestException as exc:
		assistant_reply = f"Request failed: {exc}"

	history = history + [
		{"role": "user", "content": user_message},
		{"role": "assistant", "content": assistant_reply},
	]
	return history, ""


with gr.Blocks(title="Clinical Support Copilot") as demo:
	gr.Markdown(
		"# Clinical Support Copilot\n"
		"Prototype UI connected to the AWS backend chat endpoint."
	)

	with gr.Row():
		request_type = gr.Dropdown(
			choices=["policy_answer", "admin_summary"],
			value="policy_answer",
			label="Response Type",
		)

	chatbot = gr.Chatbot(label="Chat")
	user_input = gr.Textbox(
		placeholder="Ask a policy question or request a summary...",
		label="Message",
	)

	with gr.Row():
		submit_btn = gr.Button("Send")
		clear_btn = gr.Button("Clear")

	state = gr.State([])

	submit_btn.click(
		handle_chat,
		inputs=[user_input, request_type, state],
		outputs=[chatbot, user_input],
	).then(lambda x: x, inputs=chatbot, outputs=state)

	user_input.submit(
		handle_chat,
		inputs=[user_input, request_type, state],
		outputs=[chatbot, user_input],
	).then(lambda x: x, inputs=chatbot, outputs=state)

	clear_btn.click(lambda: ([], ""), outputs=[chatbot, user_input]).then(
		lambda: [], outputs=state
	)


if __name__ == "__main__":
	demo.launch()
