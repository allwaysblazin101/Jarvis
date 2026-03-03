
def analyze_for_planning(message: str):
    msg = message.lower()

    return any(
        w in msg
        for w in [
            "plan",
            "schedule",
            "organize",
            "tomorrow",
            "later",
            "next week"
        ]
    )


def detect_financial_intent(message: str):

    msg = message.lower()

    return any(
        w in msg
        for w in [
            "money",
            "pay",
            "bill",
            "save",
            "invest",
            "budget",
            "price"
        ]
    )


def detect_relationship_intent(message: str):

    msg = message.lower()

    return any(
        w in msg
        for w in [
            "friend",
            "family",
            "relationship",
            "date",
            "love",
            "talk to"
        ]
    )

