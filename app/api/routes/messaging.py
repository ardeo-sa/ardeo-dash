"""
Messaging API endpoints for sending and retrieving messages between users.

This module defines FastAPI routes under the /api/messages prefix, allowing clients
to send a message or fetch the full message history of a specific conversation.
"""
from uuid import UUID
from typing import List
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.metrics import get_db
from app.api.schemas.messaging import MessageCreate, MessageOut
from app.services.messaging_service import create_message, get_conversation_messages

logger = logging.getLogger(__name__)
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
    logger.info("Sending message from %s to %s", message.sender_id, message.recipient_id)
    try:
        msg = create_message(db, message)
        logger.debug("Message created successfully: %s", msg)
        return msg
    except Exception as e:
        logger.exception("Error occurred while sending message: %s", e)
        raise HTTPException(status_code=500, detail="Failed to send message")


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
    logger.info("Fetching messages for conversation ID: %s", conversation_id)
    try:
        messages = get_conversation_messages(db, conversation_id)
        if not messages:
            logger.warning("No messages found for conversation ID: %s", conversation_id)
            raise HTTPException(status_code=404, detail="Conversation not found or empty")
        logger.debug("Fetched %d messages from conversation ID: %s", len(messages), conversation_id)
        return messages
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error fetching messages for conversation ID %s: %s", conversation_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch messages")

