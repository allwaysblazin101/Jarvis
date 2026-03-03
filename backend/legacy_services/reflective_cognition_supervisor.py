from services.memory_brain.master_memory_engine import (
    build_master_prompt_context
)

from services.cognitive_state_service import get_or_create_cognitive_state
from services.decision_engine_service import evaluate_decision_context


# =====================================================
# AGI SELF REFLECTION ⭐ (FINAL CORE LAYER)
# =====================================================

def reflect_and_optimize(phone_number: str, message: str, tone_score: float):

    """
    This is NOT learning new features.

    This is:
    → Evaluating system performance
    → Adjusting behavior strategy
    → Maintaining sovereign alignment with owner
    """

    cognitive_state = get_or_create_cognitive_state(phone_number)

    trust = cognitive_state.trust_score
    friendship = cognitive_state.friendship_score

    # -------------------------------
    # Reflect on communication quality
    # -------------------------------

    decision_safe = evaluate_decision_context(
        phone_number=phone_number,
        tone_score=tone_score
    )

    # Adjust response strategy heuristically
    if not decision_safe:
        return "SAFE_MODE"

    if trust < 0.4:
        return "EMPATHETIC_MODE"

    if friendship > 0.7:
        return "PERSONALIZED_FRIEND_MODE"

    return "NORMAL_MODE"