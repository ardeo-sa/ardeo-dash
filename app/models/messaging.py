"""
SQLAlchemy ORM models for the messaging feature in the healthcare web app.

Defines the `Conversation` and `Message` database tables, which support private
messaging between two users. Each conversation contains multiple messages,
and each message includes metadata such as sender, receiver, timestamp, and read status.
"""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import UUID
import datetime

from app.database import Base

class Conversation(Base):
    """
        Represents a private conversation between two users.

        Attributes:
            id (UUID): Primary key, unique identifier for the conversation.
            user1_id (UUID): ID of the first user.
            user2_id (UUID): ID of the second user.
            created_at (datetime): Timestamp of when the conversation was created.
            messages (List[Message]): One-to-many relationship to messages in this conversation.
    """
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user1_id = Column(UUID(as_uuid=True), nullable=False)
    user2_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    """
        Represents a single message sent between two users in a conversation.

        Attributes:
            id (UUID): Primary key, unique identifier for the message.
            conversation_id (UUID): Foreign key referencing the parent conversation.
            sender_id (UUID): ID of the user who sent the message.
            receiver_id (UUID): ID of the user receiving the message.
            content (str): The text content of the message.
            timestamp (datetime): Timestamp of when the message was sent.
            read (bool): Whether the message has been read by the receiver.
            conversation (Conversation): Relationship to the parent conversation.
    """
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    sender_id = Column(UUID(as_uuid=True), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)

    conversation = relationship("Conversation", back_populates="messages")
