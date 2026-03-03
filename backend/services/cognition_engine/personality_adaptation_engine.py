def adapt_personality_prompt(base_prompt: str, user_message: str):

    msg = user_message.lower()

    if any(word in msg for word in ["lol", "haha", "funny"]):
        base_prompt += "\nBe slightly humorous."

    if any(word in msg for word in ["sad", "hard", "tired"]):
        base_prompt += "\nBe empathetic and supportive."

    if any(word in msg for word in ["busy", "work"]):
        base_prompt += "\nBe short and respectful of time."

    return base_prompt
