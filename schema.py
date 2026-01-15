from datetime import datetime
from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime


class ChatMessagesResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: list[MessageResponse]


class ChatIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class MessageIn(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
