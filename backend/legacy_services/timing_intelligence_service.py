from datetime import datetime


def should_reply_now(urgency="low", hour=None):

    if hour is None:
        hour = datetime.now().hour

    # Night hours = delay non urgent messages
    if hour >= 22 or hour <= 6:
        if urgency == "high":
            return True
        return False

    # Work hours logic
    if 9 <= hour <= 17:
        if urgency == "low":
            return False
        return True

    return True
