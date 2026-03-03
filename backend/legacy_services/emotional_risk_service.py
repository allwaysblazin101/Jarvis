def detect_emotional_risk(message: str):

    message = message.lower()

    risk_keywords = [
        "mad",
        "angry",
        "upset",
        "why did you",
        "you never",
        "don't talk to me",
        "leave me alone",
        "not happy"
    ]

    risk_score = 0.3

    for word in risk_keywords:
        if word in message:
            risk_score += 0.1

    return min(risk_score, 1.0)