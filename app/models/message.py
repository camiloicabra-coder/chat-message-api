from sqlalchemy import Column, String, DateTime, JSON
from app.db.db import Base
import datetime


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    sender = Column(String, nullable=False)  # "user" o "system"
    extra_metadata = Column(JSON, nullable=True)
