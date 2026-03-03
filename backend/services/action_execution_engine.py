from typing import Dict


def detect_action_request(message: str) -> Dict:
    action_keywords = [
        "send", "email", "book", "schedule",
        "order", "pay", "call", "cancel"
    ]

    msg = message.lower()

    action_detected = any(word in msg for word in action_keywords)

    return {
        "action_requested": action_detected
    }


def execute_action_stub(action_text: str) -> str:
    """
    Placeholder until real integrations exist.
    """
    return f"Action requested: '{action_text}'. Integration not yet connected."
