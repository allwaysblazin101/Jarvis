from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database.connection import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)

    phone_number = Column(String, index=True)

    user_message = Column(String)
    ai_response = Column(String)

    # ✅ Add these (you were missing them)
    tone_score = Column(Float, default=0.5)
    urgency_score = Column(Float, default=0.5)

    timestamp = Column(DateTime, default=datetime.utcnow)