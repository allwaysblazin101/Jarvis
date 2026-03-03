def update_personality_profile(message: str):

    msg = message.lower()

    profile = {
        "style": "neutral"
    }

    if any(word in msg for word in ["lol", "haha", "funny"]):
        profile["style"] = "humorous"

    if any(word in msg for word in ["sad", "hard", "tired", "bad"]):
        profile["style"] = "empathetic"

    if any(word in msg for word in ["busy", "work"]):
        profile["style"] = "concise"

    return profile