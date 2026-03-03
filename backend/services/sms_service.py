import os
from config import TWILIO_PHONE_NUMBER, OWNER_NUMBER
from twilio.rest import Client



account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
owner_number = os.getenv("MY_PHONE_NUMBER")

client = Client(account_sid, auth_token)


# ===============================
# Generic SMS Sender
# ===============================

def send_sms(to_number: str, message: str):

    if not to_number:
        return

    client.messages.create(
        body=message,
        from_=twilio_number,
        to=to_number
    )


# ===============================
# Owner Suggestion Push
# ===============================

def send_to_owner(suggestions):

    try:
        if not owner_number:
            return

        text = "AI Suggestions:\n" + "\n".join(suggestions)

        client.messages.create(
            body=text,
            from_=twilio_number,
            to=owner_number
        )

    except Exception as e:
        print("Owner SMS push failed:", e)