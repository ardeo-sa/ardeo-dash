from uuid import UUID

from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: UUID
    sender_id: UUID
    receiver_id: UUID
    content: str
