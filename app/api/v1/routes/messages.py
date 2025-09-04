from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.message import MessageCreate, MessageResponse
from typing import List, Optional
from fastapi import Query
from app.services.message_service import process_message, get_messages
from app.core.errors import APIError

router = APIRouter()




@router.get("/messages/{session_id}", response_model=List[MessageResponse], tags=["messages"])
def list_messages(
    session_id: str,
    sender: Optional[str] = Query(None, description="Filtrar por sender: user/system"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de mensajes"),
    offset: int = Query(0, ge=0, description="Desplazamiento para paginación"),
    db: Session = Depends(get_db),
):
    try:
        messages = get_messages(db, session_id, sender, limit, offset)
        return messages
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor",
        )
@router.post("/messages", response_model=MessageResponse, tags=["messages"])
def create_message(msg: MessageCreate, db: Session = Depends(get_db)):
    try:
        new_message = process_message(db, msg)
        return new_message
    except APIError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.message),
        )
  
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor",
        )
    
