def detect_tone(message: str) -> str:
    """
    Improved rule-based tone detector with emoji weighting and length signal.
    Returns: "positive", "negative", "neutral"
    """
    if not message:
        return "neutral"

    msg = message.lower()
    msg_length = len(msg)

    # Positive indicators (words + strong emojis)
    pos_indicators = [
        "good", "great", "happy", "awesome", "love", "nice", "cool", "fun", "excited",
        "lol", "haha", "lmao", "rofl", "😂", "😆", "🤣", "😊", "😍", "❤️", "🙌", "🔥"
    ]
    pos_count = sum(1 for w in pos_indicators if w in msg)

    # Negative indicators
    neg_indicators = [
        "bad", "sad", "tired", "angry", "upset", "sorry", "hate", "annoying", "😔", "😢",
        "😠", "😞", "😭", "🥺"
    ]
    neg_count = sum(1 for w in neg_indicators if w in msg)

    # Emoji-only boost (if no words but strong emoji present)
    strong_pos_emoji = any(e in msg for e in ["😂", "😆", "🤣", "😍", "🔥"])
    strong_neg_emoji = any(e in msg for e in ["😔", "😢", "😭", "😠"])

    # Length & structure signals
    length_bonus = 1 if msg_length > 80 else 0
    short_negative_bonus = 1 if msg_length < 40 and neg_count > 0 else 0

    # Final scoring
    pos_total = pos_count + (1 if strong_pos_emoji else 0) + length_bonus
    neg_total = neg_count + (1 if strong_neg_emoji else 0) + length_bonus + short_negative_bonus

    if pos_total > neg_total + 1:
        return "positive"
    if neg_total > pos_total + 1:
        return "negative"

    return "neutral"