from database.connection import SessionLocal
from models.social_memory import SocialMemory
from datetime import datetime


# =====================================================
# EMOTION INTELLIGENCE CORE ⭐
# =====================================================

def update_emotional_state(phone_number, tone_label):

    db = SessionLocal()

    emotion_map = {
        "neutral": 0.5,
        "happy": 0.8,
        "sad": 0.2,
        "angry": 0.1,
        "flirty": 0.7,
        "excited": 0.9
    }

    tone_score = emotion_map.get(
        str(tone_label).lower(),
        0.5
    )

    memory = db.query(SocialMemory).filter(
        SocialMemory.phone_number == phone_number
    ).first()

    # =====================================================
    # NEW AGI STYLE LEARNING ⭐
    # =====================================================

    if not memory:
        memory = SocialMemory(
            phone_number=phone_number,
            emotional_score=tone_score,
            trust_score=0.5,
            relationship_strength=0.5,
            emotional_volatility=0.0,
            interaction_count=1,
            last_interaction=datetime.utcnow(),
            last_emotional_update=datetime.utcnow()
        )

        db.add(memory)

    else:

        # Emotional smoothing learning
        memory.emotional_score = (
            memory.emotional_score * 0.8 +
            tone_score * 0.2
        )

        # Relationship momentum learning
        memory.relationship_strength = min(
            1.0,
            memory.relationship_strength + 0.01
        )

        # Volatility detection ⭐
        emotion_delta = abs(memory.emotional_score - tone_score)

        memory.emotional_volatility = (
            memory.emotional_volatility * 0.7 +
            emotion_delta * 0.3
        )

        memory.interaction_count += 1

        memory.last_interaction = datetime.utcnow()
        memory.last_emotional_update = datetime.utcnow()

    db.commit()
    db.close()


# =====================================================
# EMOTIONAL SAFETY SIGNAL ⭐ (VERY IMPORTANT)
# =====================================================

def get_emotional_risk_level(phone_number):

    db = SessionLocal()

    memory = db.query(SocialMemory).filter(
        SocialMemory.phone_number == phone_number
    ).first()

    db.close()

    if not memory:
        return 0.5

    # High risk if:
    # - Low trust
    # - High emotional volatility

    risk = (
        (1 - (memory.trust_score or 0.5)) * 0.6 +
        (memory.emotional_volatility or 0.0) * 0.4
    )

    return min(max(risk, 0.0), 1.0)


# =====================================================
# RELATIONSHIP INTELLIGENCE ⭐
# =====================================================

def get_relationship_context(phone_number):

    db = SessionLocal()

    memory = db.query(SocialMemory).filter(
        SocialMemory.phone_number == phone_number
    ).first()

    db.close()

    if not memory:
        return {}

    return {
        "emotional_score": memory.emotional_score,
        "trust_score": memory.trust_score,
        "relationship_strength": memory.relationship_strength,
        "volatility": memory.emotional_volatility
    }