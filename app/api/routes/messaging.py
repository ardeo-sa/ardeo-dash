"""
Messaging API endpoints for sending and retrieving messages between users.

This module defines FastAPI routes under the /api/messages prefix, allowing clients
to send a message or fetch the full message history of a specific conversation.
"""
from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.metrics import get_db
from app.api.schemas.messaging import MessageCreate, MessageOut
from app.services.messaging_service import create_message, get_conversation_messages

router = APIRouter(prefix="/messages", tags=["Messaging"])

@router.post("/", response_model=MessageOut)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    """
    Send a new message within a conversation.

    Args:
        message (MessageCreate): The message data including sender, recipient, and content.
        db (Session): The SQLAlchemy session (injected via dependency).

    Returns:
        MessageOut: The created message with metadata (e.g., timestamp, ID).
    """
    return create_message(db, message)

@router.get("/{conversation_id}", response_model=List[MessageOut])
def fetch_messages(conversation_id: UUID, db: Session = Depends(get_db)):
    """
        Retrieve all messages from a specific conversation.

        Args:
            conversation_id (UUID): The unique identifier for the conversation.
            db (Session): The SQLAlchemy session (injected via dependency).

        Raises:
            HTTPException: 404 error if the conversation does not exist or contains no messages.

        Returns:
            List[MessageOut]: A list of messages in the conversation, ordered chronologically.
    """
    messages = get_conversation_messages(db, conversation_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Conversation not found or empty")
    return messages
