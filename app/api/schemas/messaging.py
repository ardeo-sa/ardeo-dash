from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List

class MessageCreate(BaseModel):
    conversation_id: UUID
    sender_id: UUID
    receiver_id: UUID
    content: str

class MessageOut(BaseModel):
    id: UUID
    conversation_id: UUID
    sender_id: UUID
    receiver_id: UUID
    content: str
    timestamp: datetime
    read: bool

    class Config:
        orm_mode = True

class ConversationOut(BaseModel):
    id: UUID
    user1_id: UUID
    user2_id: UUID
    created_at: datetime
    messages: List[MessageOut]

    class Config:
        orm_mode = True
