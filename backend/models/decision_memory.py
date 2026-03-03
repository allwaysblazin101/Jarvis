from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database.connection import Base


class DecisionMemory(Base):
    __tablename__ = "decision_memory"

    id = Column(Integer, primary_key=True)

    phone_number = Column(String)

    decision_type = Column(String)  # reply_now, reply_later, notify_user
    confidence_score = Column(Float)

    emotion_context = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)