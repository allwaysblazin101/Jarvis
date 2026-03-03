from sqlalchemy import Column, Integer, String, Float, DateTime
from database.connection import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_number = Column(String, unique=True, index=True)
    relationship_type = Column(String)
    importance_score = Column(Float)
    communication_frequency = Column(Float)
    last_interaction = Column(DateTime, nullable=True)