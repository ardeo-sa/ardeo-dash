from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app.schemas.messaging import MessageCreate, MessageOut
from app.services.messaging_service import create_message, get_conversation_messages

router = APIRouter(prefix="/api/messages", tags=["Messaging"])

@router.post("/", response_model=MessageOut)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    return create_message(db, message)

@router.get("/{conversation_id}", response_model=List[MessageOut])
def fetch_messages(conversation_id: UUID, db: Session = Depends(get_db)):
    messages = get_conversation_messages(db, conversation_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Conversation not found or empty")
    return messages
