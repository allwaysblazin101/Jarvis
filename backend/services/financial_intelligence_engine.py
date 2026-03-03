from typing import Dict
from services.financial_tracking_engine import log_financial_event


def detect_financial_intent(phone_number: str, message: str) -> Dict:

    keywords = [
        "money", "save", "spend", "budget",
        "invest", "income", "broke",
        "loan", "debt"
    ]

    msg = message.lower()

    detected = any(word in msg for word in keywords)

    if detected:
        log_financial_event(phone_number, message)

    return {
        "financial_related": detected
    }


def generate_financial_guardrail(message: str) -> str:
    return """
Financial Reflection:

1. Do you have 3–6 months emergency buffer?
2. Is this aligned with your long-term goals?
3. Will this increase or reduce future stress?
"""
