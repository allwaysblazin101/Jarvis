from models.conversation import Conversation
from database.connection import SessionLocal


def predict_behavior(phone_number: str):

    db = SessionLocal()

    conversations = db.query(Conversation).filter(
        Conversation.phone_number == phone_number
    ).all()

    if len(conversations) < 3:
        db.close()
        return "unknown"

    avg_length = sum(len(c.user_message) for c in conversations) / len(conversations)

    db.close()

    if avg_length > 40:
        return "detailed_talker"

    return "short_replier"
