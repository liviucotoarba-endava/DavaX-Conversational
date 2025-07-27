from models import ChatRequest


def get_current_user_message(request: ChatRequest):
    if request.image:
        return [{
            "role": "user",
            "content": [
                {"type": "input_text", "text": request.text},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{request.image}",
                },
            ],
        }]

    return [{"role": "user", "content": request.text}]
