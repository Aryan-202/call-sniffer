from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from database.database import Base

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class WebhookLog(Base):
    __tablename__ = "webhook_logs"

    id = Column(Integer, primary_key=True, index=True)
    payload = Column(JSON, nullable=False)
    type = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
