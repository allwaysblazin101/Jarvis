from database.connection import Base
from sqlalchemy import Column, Integer, String, Float, DateTime


class UserProfileMemory(Base):

    __tablename__ = "user_profile_memory"

    id = Column(Integer, primary_key=True)

    phone_number = Column(String, index=True)

    knowledge_key = Column(String)   # e.g. job, skill, preference

    knowledge_value = Column(String)

    confidence = Column(Float, default=0.5)

    timestamp = Column(DateTime)