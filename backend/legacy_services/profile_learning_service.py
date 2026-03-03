from database.connection import SessionLocal
from models.user_profile_memory import UserProfileMemory
from datetime import datetime


def learn_user_profile_fact(phone_number, message):

    db = SessionLocal()

    msg_lower = message.lower()

    # Simple knowledge extraction (can be upgraded later to NLP)
    job_keywords = [
        "renovation",
        "construction",
        "tiling",
        "drywall",
        "paint",
        "framing",
        "remodel"
    ]

    for word in job_keywords:

        if word in msg_lower:

            existing = db.query(UserProfileMemory).filter(
                UserProfileMemory.phone_number == phone_number,
                UserProfileMemory.knowledge_value == word
            ).first()

            if not existing:

                db.add(UserProfileMemory(
                    phone_number=phone_number,
                    knowledge_key="occupation_skill",
                    knowledge_value=word,
                    confidence=0.8,
                    timestamp=datetime.utcnow()
                ))

    db.commit()
    db.close()