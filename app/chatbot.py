import base64
import io
import os
from collections import deque

from openai import OpenAI

from models import ChatRequest, ChatResponse

openAIClient = OpenAI(api_key=os.getenv("ENDAVA_OPENAI_API_KEY"))

instruction: str = "Keep your answers simple and concise, under 50 words"
developer_prompt: str = (
    "You are a helpful chatbot/assistant that answers user's questions"
)

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
    )
    history.append({"role": "assistant", "content": response.output_text})

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
        input=_get_current_user_message(request),
        max_output_tokens=500,
        store=True,
        tools=[
            {
                "type": "image_generation",
                "background": "transparent",
                "quality": "high",
                "output_format": "png",
            }
        ],
    )

    print(f"Previous response ID: {response.previous_response_id}")
    print(f"Input tokens: {response.usage.input_tokens}")
    print(f"Output tokens: {response.usage.output_tokens}")
    previous_response_id = response.id

    image_generation_calls = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]
    image_response = (
        image_generation_calls[0]
        if image_generation_calls and image_generation_calls[0]
        else None
    )
    audio_response = _generate_audio_response(response.output_text)

    return ChatResponse(
        text=response.output_text, image=image_response, audio=audio_response
    )


def _get_current_user_message(request: ChatRequest):
    content = [{"type": "input_text", "text": request.text}]

    if request.audio:
        transcription = _transcribe_from_audio_request(request.audio)
        content.append(
            {"type": "input_text", "text": f"Transcription from audio: {transcription}"}
        )

    if request.image:
        content.append(
            {
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{request.image}",
            }
        )

    return [{"role": "user", "content": content}]


def _generate_audio_response(text: str):
    response = openAIClient.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="echo",
        input=text,
        instructions="Speak in a cheerful and positive tone.",
    )
    return base64.b64encode(response.content).decode()


def _transcribe_from_audio_request(audio):
    audio_bytes = base64.b64decode(audio)
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.mp3"
    transcription = openAIClient.audio.transcriptions.create(
        model="gpt-4o-transcribe", file=audio_file
    )
    print(f"Transcription: {transcription.text}")
    return transcription.text
