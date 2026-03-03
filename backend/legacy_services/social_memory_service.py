from database.connection import SessionLocal
from models.social_memory import SocialMemory
from datetime import datetime


def update_social_memory(phone_number, tone_score=0.5):

    db = SessionLocal()

    memory = db.query(SocialMemory).filter(
        SocialMemory.phone_number == phone_number
    ).first()

    # If first time interacting
    if not memory:
        memory = SocialMemory(
            phone_number=phone_number,
            emotional_score=tone_score,
            trust_score=0.5,
            relationship_strength=0.5
        )
        db.add(memory)

    else:
        # Slowly update memory (VERY IMPORTANT)
        memory.emotional_score = (
            memory.emotional_score + tone_score
        ) / 2

        memory.last_interaction = datetime.utcnow()

    db.commit()
    db.close()