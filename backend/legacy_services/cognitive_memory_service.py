from database.connection import SessionLocal
from models.cognitive_state import CognitiveState
from datetime import datetime


def update_cognitive_memory(
    phone_number: str,
    tone_score: float,
    message_length: int
):

    db = SessionLocal()

    state = db.query(CognitiveState).filter(
        CognitiveState.phone_number == phone_number
    ).first()

    if not state:
        state = CognitiveState(
            phone_number=phone_number,
            trust_score=0.5,        # neutral baseline
            friendship_score=0.3    # early-stage connection
        )
        db.add(state)
        db.commit()   # commit so defaults persist

    # -----------------------------
    # Normalize values (Safety Layer)
    # -----------------------------

    state.trust_score = state.trust_score or 0.5
    state.friendship_score = state.friendship_score or 0.3
    tone_score = tone_score or 0.0
    message_length = message_length or 0

    # -----------------------------
    # Reinforcement Learning Style Updates
    # -----------------------------

    trust_delta = (tone_score * 0.6) + (message_length * 0.0002)

    state.trust_score = min(
        1.0,
        (state.trust_score * 0.7) + (trust_delta * 0.3)
    )

    state.friendship_score = min(
        1.0,
        state.friendship_score + (message_length * 0.0003)
    )

    state.emotional_state_vector = {
        "last_tone": tone_score,
        "message_length": message_length,
        "timestamp": datetime.utcnow().isoformat()
    }

    state.last_updated = datetime.utcnow()

    db.commit()
    db.close()