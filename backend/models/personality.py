from sqlalchemy import Column, Integer, Float, String
from database.connection import Base


class PersonalityProfile(Base):
    __tablename__ = "personality_profiles"

    id = Column(Integer, primary_key=True)

    avg_message_length = Column(Float, default=0.0)
    emotional_openness = Column(Float, default=0.5)
    casualness_score = Column(Float, default=0.5)
    response_style = Column(String, default="neutral")