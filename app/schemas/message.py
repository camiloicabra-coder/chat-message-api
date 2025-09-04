from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Literal


class MessageBase(BaseModel):
    message_id: str = Field(..., example="msg-123456")
    session_id: str = Field(..., example="session-abcdef")
    content: str = Field(..., example="Hola, ¿cómo puedo ayudarte hoy?")
    timestamp: datetime = Field(..., example="2023-06-15T14:30:00Z")
    sender: Literal["user", "system"]
    extra_metadata: Optional[Dict] = None 

class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    extra_metadata: Optional[Dict] = None

    class Config:
        orm_mode = True

class MessageRead(MessageBase):
    pass