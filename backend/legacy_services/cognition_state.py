cognition = {
    "planning": {"requires_planning": False},
    "financial": {"financial_related": False},
    "action": {"action_requested": False}
}

def update_cognition_flags(message: str):
    global cognition

    msg = message.lower()

    cognition["planning"]["requires_planning"] = any(
        w in msg for w in ["plan", "schedule", "organize"]
    )

    cognition["financial"]["financial_related"] = any(
        w in msg for w in ["money", "pay", "save", "invest", "bill"]
    )

    cognition["action"]["action_requested"] = any(
        w in msg for w in ["order", "buy", "send", "book"]
    )

    return cognition
