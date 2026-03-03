import os
from database.connection import SessionLocal
from models.contact import Contact
from models.cognitive_state import CognitiveState


def seed_owner_profile():
    db = SessionLocal()

    owner_number = os.getenv("OWNER_NUMBER")

    if not owner_number:
        print("OWNER_NUMBER not set in .env")
        return

    existing = db.query(Contact).filter(
        Contact.phone_number == owner_number
    ).first()

    if not existing:
        db.add(Contact(
            name="Owner",
            phone_number=owner_number,
            relationship_type="owner",
            importance_score=1.0,
            communication_frequency=0.0
        ))

    db.commit()
    db.close()


def seed_owner_cognitive_state():
    db = SessionLocal()

    owner_number = os.getenv("OWNER_NUMBER")

    existing = db.query(CognitiveState).filter(
        CognitiveState.phone_number == owner_number
    ).first()

    if not existing:
        db.add(CognitiveState(
            phone_number=owner_number,
            trust_score=1.0,
            friendship_score=1.0,
            emotional_state_vector="owner_trusted",
            response_preference_profile="friendly",
            interaction_latency_pattern="normal"
        ))

    db.commit()
    db.close()
