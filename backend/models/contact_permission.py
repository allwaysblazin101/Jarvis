from sqlalchemy import Column, Integer, String, Boolean, Float
from database.connection import Base


class ContactPermission(Base):
    __tablename__ = "contact_permissions"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=True)

    phone_number = Column(String, unique=True, index=True)

    relationship_type = Column(String, default="unknown")

    priority_score = Column(Float, default=50.0)

    allowed = Column(Boolean, default=False)