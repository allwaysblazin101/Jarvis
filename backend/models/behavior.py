from sqlalchemy import Column, Integer, String, Float
from database.connection import Base


class BehaviorPattern(Base):
    __tablename__ = "behavior_patterns"

    id = Column(Integer, primary_key=True)

    pattern_type = Column(String)
    pattern_value = Column(Float)
