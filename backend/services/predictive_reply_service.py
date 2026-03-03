from database.connection import SessionLocal
from models.decision_memory import DecisionMemory


def predict_reply_score(message_length, trust_score, friendship_score):

    # Simple ML-style heuristic ranking
    return (
        (trust_score * 0.5) +
        (friendship_score * 0.3) +
        (message_length * 0.0001)
    )


def learn_from_selection(phone_number, selected_index):

    db = SessionLocal()

    memory = db.query(DecisionMemory).filter(
        DecisionMemory.phone_number == phone_number
    ).first()

    if memory:
        memory.selection_success_count += 1

    db.commit()
    db.close()