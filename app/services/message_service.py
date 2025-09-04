import datetime
from sqlalchemy.orm import Session
from app.schemas.message import MessageCreate
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.message import Message
from app.core.errors import APIError



def get_messages(
    db: Session,
    session_id: str,
    sender: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> List[Message]:
    query = db.query(Message).filter(Message.session_id == session_id)

    if sender:
        query = query.filter(Message.sender == sender)

    return query.offset(offset).limit(limit).all()

# Lista simple de palabras prohibidas
BANNED_WORDS = ["malo", "inapropiado", "grosería"]


def process_message(db: Session, msg: MessageCreate) -> Message:
    if msg.sender not in ["user", "system"]:
        raise APIError(
            code="INVALID_FORMAT",
            message="Formato de mensaje inválido",
            details="El campo 'sender' debe ser 'user' o 'system'",
            http_status=400,
        )
    # Validar palabras prohibidas
    for banned in BANNED_WORDS:
        if banned in msg.content.lower():
             raise APIError(
                code="INVALID_CONTENT",
                message="Contenido inapropiado detectado",
                details=f"El mensaje contiene la palabra prohibida '{banned}'",
                http_status=400,
            )

    # Calcular metadatos
    extra_metadata = {
        "word_count": len(msg.content.split()),
        "character_count": len(msg.content),
        "processed_at": datetime.datetime.utcnow().isoformat(),
    }

    db_message = Message(
        message_id=msg.message_id,
        session_id=msg.session_id,
        content=msg.content,
        timestamp=msg.timestamp,
        sender=msg.sender,
        extra_metadata=extra_metadata,  # Cambiado aquí
    )

    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

