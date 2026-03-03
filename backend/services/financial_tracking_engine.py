from database.connection import SessionLocal
from models.user_profile_memory import UserProfileMemory


def log_financial_event(phone_number: str, message: str):

    db = SessionLocal()

    db.add(
        UserProfileMemory(
            phone_number=phone_number,
            memory_type="financial_event",
            content=message
        )
    )

    db.commit()
    db.close()


def get_financial_history(phone_number: str):

    db = SessionLocal()

    events = db.query(UserProfileMemory).filter(
        UserProfileMemory.phone_number == phone_number,
        UserProfileMemory.memory_type == "financial_event"
    ).all()

    db.close()

    return [e.content for e in events]
