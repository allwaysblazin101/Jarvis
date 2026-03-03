import asyncio

from services.emotional_ai_service import update_emotional_state
from services.self_reflection_engine import evaluate_self_performance
from services.decision_engine_service import evaluate_decision_context
from services.intent_prediction_engine import predict_user_intent
from services.pattern_service import update_pattern

from services.planning_engine import analyze_for_planning
from services.financial_intelligence_engine import detect_financial_intent
from services.action_execution_engine import detect_action_request


async def consciousness_cycle(
    phone_number: str,
    message: str,
    tone: str,
    risk_score: float = 0.0
):

    # Emotional perception
    update_emotional_state(phone_number, tone)

    # Intent prediction
    intent_score = predict_user_intent(pattern_type=tone)

    # Planning detection
    planning_data = analyze_for_planning(phone_number, message)

    # Financial detection
    financial_data = detect_financial_intent(phone_number, message)

    # Action detection
    action_data = detect_action_request(message)

    # Safety decision layer
    safe_to_respond = evaluate_decision_context(
        phone_number,
        tone_score=0.8 if tone != "neutral" else 0.5,
        risk_score=risk_score
    )


    return {
        "safe": safe_to_respond,
        "planning": planning_data,
        "financial": financial_data,
        "action": action_data
    }



