import os
from collections import deque

from openai import OpenAI

from models import ChatRequest, ChatResponse

openAIClient = OpenAI(
    api_key=os.getenv('ENDAVA_OPENAI_API_KEY'),
    timeout=20
)

instruction: str = "Keep your answers simple and concise, under 50 words"
developer_prompt: str = "You are a helpful chatbot/assistant that answers user's questions"

# history = [{"role": "developer", "content": developer_prompt}]
history: deque = deque([{"role": "developer", "content": developer_prompt}], maxlen=10)
previous_response_id = None


def process_message_with_history_local(request: ChatRequest) -> ChatResponse:
    history.append({"role": "user", "content": request.text})
    response = openAIClient.responses.create(
        model="gpt-4.1-mini",
        instructions=instruction,
        input=list(history),
        max_output_tokens=500,
        store=False,
        temperature=0.1
    )
    history.append({"role": "assistant", "content": response.output_text})

    print()
    print(f"History size: {len(history)}")
    print(f"History content: {history}")
    print(f"Input tokens: {response.usage.input_tokens}")
    print(f"Output tokens: {response.usage.output_tokens}")

    return ChatResponse(text=response.output_text, image=None, audio=None)


def process_message_with_history_cloud(request: ChatRequest) -> ChatResponse:
    global previous_response_id
    response = openAIClient.responses.create(
        model="gpt-4.1-mini",
        instructions=instruction,
        previous_response_id=previous_response_id,
        input=request.text,
        max_output_tokens=500,
        store=True,
        temperature=0.1
    )

    print()
    print(f"Previous response ID: {response.previous_response_id}")
    print(f"Input tokens: {response.usage.input_tokens}")
    print(f"Output tokens: {response.usage.output_tokens}")
    previous_response_id = response.id

    return ChatResponse(text=response.output_text, image=None, audio=None)

# TODO: Add image input-output support via base64 encoding in Responses API: https://platform.openai.com/docs/guides/images-vision?api-mode=responses
# TODO: Add audio input-output support via base64 encoding in Completions API: https://platform.openai.com/docs/guides/audio
