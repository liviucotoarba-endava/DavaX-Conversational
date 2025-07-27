from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    text: str
    image: Optional[str] = None
    audio: Optional[str] = None


class ChatResponse(BaseModel):
    text: str
    image: Optional[str] = None
    audio: Optional[str] = None
