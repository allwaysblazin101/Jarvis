
import datetime

def predict_user_future_needs(message: str):

    msg = message.lower()

    predictions = []

    if "work" in msg:
        predictions.append("You may want to review productivity schedule.")

    if "money" in msg:
        predictions.append("Financial monitoring recommended.")

    if "tired" in msg:
        predictions.append("Rest + sleep schedule optimization suggested.")

    return predictions

