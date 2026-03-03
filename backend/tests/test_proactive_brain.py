import pytest
from services.proactive_brain.proactive_brain_engine import should_proactively_message


def test_proactive_decision_logic():

    result = should_proactively_message(
        last_interaction_hours=72,
        emotional_score=0.7,
        trust_score=0.8,
        relationship_strength=0.8
    )

    assert isinstance(result, bool)