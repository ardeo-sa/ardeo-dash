from sqlalchemy.orm import Session
from uuid import UUID
from app.models.messaging import Message, Conversation
from app.schemas.messaging import MessageCreate
from datetime import datetime

def create_message(db: Session, msg_data: MessageCreate) -> Message:
    msg = Message(**msg_data.dict())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_conversation_messages(db: Session, conversation_id: UUID):
    return db.query(Message).filter_by(conversation_id=conversation_id).order_by(Message.timestamp).all()

