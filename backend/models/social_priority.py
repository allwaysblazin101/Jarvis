from sqlalchemy import Column, Integer, String, Float
from database.connection import Base


class SocialPriority(Base):
    __tablename__ = "social_priorities"

    id = Column(Integer, primary_key=True)

    phone_number = Column(String, unique=True)

    priority_score = Column(Float, default=50.0)

    message_frequency = Column(Float, default=0.0)

    response_speed_score = Column(Float, default=50.0)
