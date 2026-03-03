from database.connection import SessionLocal
from models.social_priority import SocialPriority


def update_social_priority(phone_number: str, message_length: int):

    if not phone_number:
        return

    db = SessionLocal()

    contact = db.query(SocialPriority).filter(
        SocialPriority.phone_number == phone_number
    ).first()

    if not contact:
        contact = SocialPriority(
            phone_number=phone_number,
            priority_score=50.0,
            message_frequency=1.0,
            response_speed_score=50.0
        )
        db.add(contact)

    # Safe math (VERY IMPORTANT)
    contact.priority_score = (contact.priority_score or 50) + 0.1

    db.commit()
    db.close()