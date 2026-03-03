from database.connection import SessionLocal
from models.decision_memory import DecisionMemory
from models.cognitive_state import CognitiveState


# =====================================================
# DECISION LOGGING
# =====================================================

def log_decision(phone_number, decision_type, confidence, emotion):

    db = SessionLocal()

    decision = DecisionMemory(
        phone_number=phone_number,
        decision_type=decision_type,
        confidence_score=float(confidence),
        emotion_context=str(emotion)
    )

    db.add(decision)
    db.commit()
    db.close()


# =====================================================
# GOD TIER DECISION SAFETY + EMPATHY GATE
# =====================================================

def evaluate_decision_context(phone_number: str,
                              tone_score: float,
                              risk_score: float = 0.0):

    db = SessionLocal()

    state = db.query(CognitiveState).filter(
        CognitiveState.phone_number == phone_number
    ).first()

    if not state:
        db.close()
        return True

    trust = state.trust_score or 0.5
    friendship = state.friendship_score or 0.5

    db.close()

    # -----------------------------
    # Emotional Safety Logic
    # -----------------------------

    # If user is emotionally unstable → increase empathy
    if tone_score < 0.4:
        return True

    # If trust is low → be cautious with decisions
    if trust < 0.3 and risk_score > 0.5:
        return False

    # If high trust → allow more direct responses
    if trust > 0.7:
        return True

    # Default safety
    if risk_score > 0.7:
        return False

    return True


# =====================================================
# EMPATHY DECISION GATE ⭐
# =====================================================

def should_use_empathy(trust_score: float, tone_score: float) -> bool:

    if tone_score < 0.4:
        return True

    if trust_score > 0.6:
        return True

    return False


# =====================================================
# REINFORCEMENT FEEDBACK LEARNING ⭐ (IMPORTANT)
# =====================================================

def update_decision_feedback(phone_number: str,
                             decision_type: str,
                             user_feedback_reward: float):

    db = SessionLocal()

    db.add(
        DecisionMemory(
            phone_number=phone_number,
            decision_type=decision_type,
            confidence_score=user_feedback_reward,
            emotion_context="feedback_learning"
        )
    )

    db.commit()
    db.close()