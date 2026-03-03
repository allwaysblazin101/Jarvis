from database.connection import SessionLocal
from models.behavior import BehaviorPattern


def predict_user_intent(pattern_type: str):

    db = SessionLocal()

    pattern = db.query(BehaviorPattern).filter(
        BehaviorPattern.pattern_type == pattern_type
    ).first()

    db.close()

    if not pattern:
        return 0.5

    return (
        pattern.pattern_value * 0.6 +
        pattern.confidence_score * 0.3 +
        pattern.recency_score * 0.1
    )
