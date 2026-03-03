from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from database.connection import Base


class PendingSuggestion(Base):

    __tablename__ = "pending_suggestions"

    id = Column(Integer, primary_key=True)

    phone_number = Column(String, index=True)

    original_message = Column(String)

    suggestion_1 = Column(String)
    suggestion_2 = Column(String)
    suggestion_3 = Column(String)

    selected_reply_index = Column(Integer, nullable=True)

    prediction_confidence = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)