from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database.connection import Base


class SocialMemory(Base):
    __tablename__ = "social_memory"

    id = Column(Integer, primary_key=True)

    phone_number = Column(String, unique=True)

    emotional_score = Column(Float, default=0.5)
    trust_score = Column(Float, default=0.5)
    relationship_strength = Column(Float, default=0.5)

    last_interaction = Column(DateTime, default=datetime.utcnow)
    last_emotional_update = Column(DateTime, default=datetime.utcnow)