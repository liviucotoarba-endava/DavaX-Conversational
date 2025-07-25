import traceback

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import chatbot as chatbot
from models import ChatRequest

app = FastAPI(
    title="Multimodal Chatbot API",
    description="AI chatbot supporting text, image and audio messages",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        return chatbot.process_message_with_history_local(request)
    except Exception as e:
        print(f"Error processing chat request: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", status_code=200)
async def health_check():
    return {"status": "up"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181)
