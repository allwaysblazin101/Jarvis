from datetime import datetime
from database.connection import SessionLocal
from models.social_memory import SocialMemory


def update_life_rhythm(phone_number: str):

    db = SessionLocal()

    memory = db.query(SocialMemory).filter(
        SocialMemory.phone_number == phone_number
    ).first()

    if not memory:
        db.close()
        return

    hour = datetime.utcnow().hour

    # Learn daily activity patterns
    memory.activity_pattern_score = (
        memory.activity_pattern_score * 0.8 +
        (hour / 24) * 0.2
    )

    db.commit()
    db.close()
