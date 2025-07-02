from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None
    audio: Optional[str] = None


class ChatResponse(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None
    audio: Optional[str] = None
