"""
Messaging service module for handling conversation messages in the healthcare web app.

This module provides functions to create and retrieve messages associated with
user conversations stored in the metrics database. It interacts with the SQLAlchemy ORM
models and is used by the FastAPI messaging routes.

Functions:
    - create_message: Stores a new message in the database.
    - get_conversation_messages: Retrieves all messages for a given conversation, ordered chronologically.
"""
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.messaging import Message, Conversation
from app.schemas.messaging import MessageCreate
# from datetime import datetime

def create_message(db: Session, message: MessageCreate) -> Message:
    """
        Create a new message in the database.

        Args:
            db (Session): The SQLAlchemy session.
            message (MessageCreate): The message data.

        Returns:
            MessageOut: The created message.
    """
    msg = Message(
        conversation_id=message.conversation_id,
        sender_id=message.sender_id,
        content=message.content,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    return msg


def get_conversation_messages(db: Session, conversation_id: UUID):
    """
    Retrieve all messages from a specific conversation.

    Args:
        db (Session): The SQLAlchemy session.
        conversation_id (UUID): The conversation ID.

    Returns:
        List[MessageOut]: List of messages in the conversation.
    """
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
