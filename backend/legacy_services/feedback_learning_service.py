
from database.connection import SessionLocal
from models.feedback import UserFeedback
from models.cognitive_state import CognitiveState


def process_feedback_and_update_trust(phone_number: str):

    db = SessionLocal()

    feedback = db.query(UserFeedback)\
        .filter(UserFeedback.phone_number == phone_number)\
        .order_by(UserFeedback.timestamp.desc())\
        .first()

    if not feedback:
        db.close()
        return

    cognitive_state = db.query(CognitiveState)\
        .filter(CognitiveState.phone_number == phone_number)\
        .first()

    if not cognitive_state:
        db.close()
        return

    # -------------------------
    # Memory Quality Learning
    # -------------------------

    old_trust = cognitive_state.trust_score or 0.5
    reward = feedback.helpful_score

    # Simple decay + reinforcement learning style update
    new_trust = (old_trust * 0.9) + (reward * 0.1)

    cognitive_state.trust_score = new_trust

    db.commit()
    db.close()

