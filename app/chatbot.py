import os
from collections import deque

from openai import OpenAI

from models import ChatRequest, ChatResponse

openAIClient = OpenAI(
    api_key=os.getenv('ENDAVA_OPENAI_API_KEY'),
    timeout=20
)

instruction: str = "Keep your answers funny, sarcastic or ironic."
system_prompt: str = "You are a helpful assistant that answers user's questions."

previous_response_id = None
history: deque = deque([{"role": "system", "content": system_prompt}], maxlen=10)


def process_message_with_local_history(request: ChatRequest) -> ChatResponse:
    history.append({"role": "user", "content": request.text})
    print(history)

    response = openAIClient.responses.create(
        model="gpt-4.1-mini",
        instructions=instruction,
        input=list(history),
        max_output_tokens=500,
        store=False,
        temperature=0.1
    )

    print(response)
    history.extend([{"role": r.role, "content": r.content} for r in response.output])
    print(history)

    return ChatResponse(text=response.output_text, image=None, audio=None)


def process_message_with_cloud_history(request: ChatRequest) -> ChatResponse:
    global previous_response_id
    print(previous_response_id)

    response = openAIClient.responses.create(
        model="gpt-4.1-mini",
        instructions=instruction,
        previous_response_id=previous_response_id,
        input=request.text,
        max_output_tokens=500,
        store=True,
        temperature=0.1
    )

    print(response)

    previous_response_id = response.id

    return ChatResponse(text=response.output_text, image=None, audio=None)
