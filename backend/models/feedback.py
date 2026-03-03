
from sqlalchemy import Column, Integer, String, Float, DateTime
from database.connection import Base
from datetime import datetime


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)

    phone_number = Column(String, index=True)

    # Was AI helpful?
    helpful_score = Column(Float, default=0.5)

    # Optional user sentiment after response
    sentiment_score = Column(Float, default=0.5)

    timestamp = Column(DateTime, default=datetime.utcnow)

