from database.connection import SessionLocal
from models.conversation import Conversation


def record_conversation(message, response, phone_number):

    db = SessionLocal()

    conv = Conversation(
        user_message=message,
        ai_response=response,
        contact_phone=phone_number
    )

    db.add(conv)
    db.commit()
    db.close()
