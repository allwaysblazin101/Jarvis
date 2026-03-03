from datetime import datetime

# These imports are placeholders — replace with actual implementations
from services.cognition_engine.trust_engine import calculate_trust_score
from services.cognition_engine.friendship_growth_engine import calculate_friendship_growth
from services.timing_intelligence_service import should_reply_now


def should_proactively_message(
    last_interaction_hours: float,
    emotional_score: float,
    trust_score: float,
    relationship_strength: float
) -> bool:
    """
    Decide whether to send a proactive message.
    Returns True if conditions are favorable.
    """
    # Timing check
    current_hour = datetime.now().hour
    timing_ok = should_reply_now(urgency=0.2, hour=current_hour)

    # Derived social signals
    friendship_growth = calculate_friendship_growth(emotional_score, relationship_strength)
    trust_level = calculate_trust_score(trust_score, relationship_strength)

    # Decision rules (tunable thresholds)
    if friendship_growth > 0.65 and trust_level > 0.65 and timing_ok:
        return True

    # Long silence fallback (very high trust)
    if last_interaction_hours > 72 and trust_level > 0.75:
        return True

    return False