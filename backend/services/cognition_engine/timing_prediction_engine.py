from models.conversation import Conversation
from database.connection import SessionLocal
from datetime import datetime


def predict_next_interaction_time(phone_number: str):

    db = SessionLocal()

    conversations = db.query(Conversation).filter(
        Conversation.phone_number == phone_number
    ).order_by(Conversation.timestamp.desc()).all()

    if len(conversations) < 2:
        db.close()
        return 24

    gaps = []

    for i in range(len(conversations) - 1):
        gap = conversations[i].timestamp - conversations[i+1].timestamp
        gaps.append(gap.total_seconds())

    avg_gap = sum(gaps) / len(gaps)

    db.close()

    return avg_gap / 3600
