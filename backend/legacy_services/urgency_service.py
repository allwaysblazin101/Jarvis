def detect_urgency(message: str) -> str:
    """
    Simple but slightly expanded urgency detector.
    Returns: "high", "medium", "low"
    """
    if not message:
        return "low"

    msg = message.lower()

    # High urgency (immediate danger/help needed)
    high_urgency = [
        "emergency", "hospital", "help", "urgent", "call me", "not good",
        "something happened", "dying", "hurt", "accident", "911", "now!!"
    ]

    # Medium urgency (needs attention soon)
    medium_urgency = [
        "important", "talk now", "need to talk", "asap", "quickly", "please help",
        "worried", "stressed", "bad day", "really need"
    ]

    # Quick scan
    if any(word in msg for word in high_urgency):
        return "high"

    if any(word in msg for word in medium_urgency):
        return "medium"

    # Bonus: multiple exclamation/question marks or all caps
    if "!!!" in msg or "???" in msg or msg.isupper() and len(msg) > 10:
        return "medium"

    return "low"