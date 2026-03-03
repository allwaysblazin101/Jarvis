from twilio.rest import Client
import os

class SMSTool:
    def __init__(self):
        self.client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")

    async def read_recent_sms(self, limit=5):
        messages = self.client.messages.list(
            to=self.from_number,
            limit=limit
        )
        return [
            {"from": m.from_, "body": m.body, "date": str(m.date_sent)}
            for m in messages
        ]

    async def send_sms(self, to_number: str, message: str):
        self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=to_number
        )
        print(f"Sent to {to_number}: {message}")
