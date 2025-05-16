"""
Pydantic schemas for messaging functionality.

This module defines the data models used for creating, retrieving, and serializing
messages and conversations between users. These schemas support data validation
and automatic documentation generation for FastAPI endpoints related to messaging.

Schemas:
- MessageCreate: For creating a new message.
- MessageOut: For returning message data via the API.
- ConversationOut: For returning a conversation along with its messages.
- ConversationCreate: For initiating a new conversation between two users.
"""
from uuid import UUID
from datetime import datetime
from typing import List
from pydantic import BaseModel

class MessageCreate(BaseModel):
    """
        Schema for creating a new message.

        Attributes:
            conversation_id (UUID): The ID of the conversation the message belongs to.
            sender_id (UUID): The ID of the user sending the message.
            receiver_id (UUID): The ID of the user receiving the message.
            content (str): The content of the message.
    """
    conversation_id: UUID
    sender_id: UUID
    receiver_id: UUID
    content: str

    class Config:
        """
            Enables ORM mode for converting SQLAlchemy objects to Pydantic models.
        """
        orm_mode = True


class MessageOut(BaseModel):
    """
        Schema for returning a message from the API.

        Attributes:
            id (UUID): Unique identifier for the message.
            conversation_id (UUID): The ID of the conversation the message belongs to.
            sender_id (UUID): The ID of the user who sent the message.
            receiver_id (UUID): The ID of the user who received the message.
            content (str): The content of the message.
            timestamp (datetime): When the message was sent.
            read (bool): Whether the message has been read by the receiver.
    """
    id: UUID
    timestamp: datetime
    read: bool

    class Config:
        """
            Enables ORM mode for converting SQLAlchemy objects to Pydantic models.
        """
        orm_mode = True


class ConversationOut(BaseModel):
    """
        Schema for returning a conversation with its messages.

        Attributes:
            id (UUID): Unique identifier for the conversation.
            user1_id (UUID): The ID of the first user in the conversation.
            user2_id (UUID): The ID of the second user in the conversation.
            created_at (datetime): When the conversation was created.
            messages (List[MessageOut]): List of messages exchanged in this conversation.
    """
    id: UUID
    user1_id: UUID
    user2_id: UUID
    created_at: datetime
    messages: List[MessageOut]

    class Config:
        """
            Enables ORM mode for converting SQLAlchemy objects to Pydantic models.
        """
        orm_mode = True


class ConversationCreate(BaseModel):
    """
    Schema for creating a new conversation between two users.

    Attributes:
        user1_id (UUID): The ID of the first user initiating the conversation.
        user2_id (UUID): The ID of the second user in the conversation.
    """
    user1_id: UUID
    user2_id: UUID

    class Config:
        """
            Enables ORM mode for converting SQLAlchemy objects to Pydantic models.
        """
        orm_mode = True
