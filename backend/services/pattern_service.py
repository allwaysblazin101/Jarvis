from datetime import datetime
from database.connection import SessionLocal
from models.behavior import BehaviorPattern


# =====================================================
# GOD TIER BEHAVIOR PATTERN LEARNING
# =====================================================

def update_pattern(pattern_type: str,
                   value: float,
                   confidence: float = 0.8):

    db = SessionLocal()

    pattern = db.query(BehaviorPattern).filter(
        BehaviorPattern.pattern_type == pattern_type
    ).first()

    now = datetime.utcnow()

    # ------------------------------------------------
    # If pattern does not exist → Create new memory
    # ------------------------------------------------

    if not pattern:

        pattern = BehaviorPattern(
            pattern_type=pattern_type,
            pattern_value=value,
            confidence_score=confidence,
            last_updated=now,
            recency_score=1.0
        )

        db.add(pattern)

    else:

        # ------------------------------------------------
        # Temporal Recency Learning
        # ------------------------------------------------

        time_diff = (now - pattern.last_updated).total_seconds() / 3600

        # Recency decay (older memories learn slower)
        decay_factor = min(1.0, 1.0 / (1.0 + time_diff))

        # ------------------------------------------------
        # Reinforcement Learning Style Update
        # ------------------------------------------------

        pattern.pattern_value = (
            pattern.pattern_value * (0.85 * decay_factor) +
            value * (0.15 + (confidence * 0.2))
        )

        # Update confidence
        pattern.confidence_score = (
            pattern.confidence_score * 0.9 +
            confidence * 0.1
        )

        pattern.recency_score = min(
            1.0,
            pattern.recency_score + 0.05
        )

        pattern.last_updated = now

    db.commit()
    db.close()


# =====================================================
# PATTERN PREDICTION BRAIN ⭐
# =====================================================

def predict_pattern(pattern_type: str) -> float:

    db = SessionLocal()

    pattern = db.query(BehaviorPattern).filter(
        BehaviorPattern.pattern_type == pattern_type
    ).first()

    db.close()

    if not pattern:
        return 0.5

    # Prediction = weighted intelligence score
    return (
        pattern.pattern_value * 0.6 +
        pattern.confidence_score * 0.3 +
        pattern.recency_score * 0.1
    )