"""
Trust cognition engine
Handles trust scoring between AI and user.
"""


def update_trust_score(phone_number: str, interaction_quality: float = 0.7):

    # Placeholder trust learning logic (you can improve later with ML)
    print(f"Updating trust score for {phone_number} -> {interaction_quality}")

    return {
        "trust_score": interaction_quality
    }


def calculate_trust_score(message_length: int = 0, emotional_score: float = 0.5):
    """
    Simple trust heuristic model (MVP version)
    """

    # Basic trust logic
    base_trust = 0.5

    # Longer conversations usually build trust
    length_bonus = min(message_length / 200, 0.2)

    # Emotional safety increases trust
    emotion_bonus = emotional_score * 0.3

    return min(base_trust + length_bonus + emotion_bonus, 1.0)
