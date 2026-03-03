from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database.connection import Base


class BehaviorFeedback(Base):

    __tablename__ = "behavior_feedback"

    id = Column(Integer, primary_key=True)

    phone_number = Column(String, index=True)

    ai_response = Column(String)

    # User reaction score (-1 bad → 1 good)
    acceptance_score = Column(Float, default=0.0)

    # Did user continue conversation?
    conversation_continued = Column(Float, default=0.0)

    timestamp = Column(DateTime, default=datetime.utcnow)
