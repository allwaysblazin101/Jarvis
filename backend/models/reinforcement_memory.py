from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database.connection import Base


class ReinforcementMemory(Base):

    __tablename__ = "reinforcement_memory"

    id = Column(Integer, primary_key=True)

    phone_number = Column(String)

    candidate_reply = Column(String)

    predicted_score = Column(Float)

    actual_reward = Column(Float)

    prediction_error = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)