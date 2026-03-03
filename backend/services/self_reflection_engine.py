from database.connection import SessionLocal
from models.cognitive_state import CognitiveState


def evaluate_self_performance(phone_number: str, satisfaction_score: float):

    db = SessionLocal()

    state = db.query(CognitiveState).filter(
        CognitiveState.phone_number == phone_number
    ).first()

    if not state:
        db.close()
        return

    # Self improvement loop
    state.trust_score = (
        state.trust_score * 0.9 +
        satisfaction_score * 0.1
    )

    state.friendship_score = min(
        1.0,
        state.friendship_score + (satisfaction_score * 0.02)
    )

    db.commit()
    db.close()
