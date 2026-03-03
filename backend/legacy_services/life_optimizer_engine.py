
def generate_life_suggestion(message: str):

    msg = message.lower()

    suggestions = []

    if "money" in msg or "save" in msg:
        suggestions.append("Consider setting a 20% automatic savings rule.")

    if "exercise" in msg or "health" in msg:
        suggestions.append("Try 30 minutes of walking today.")

    if "stress" in msg:
        suggestions.append("Take 5 deep breaths before responding to messages.")

    return "\n".join(suggestions)

