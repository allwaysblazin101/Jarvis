from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from database.connection import SessionLocal
from models.conversation import Conversation
from models.contact import Contact

from services.sms_service import send_sms


def check_relationship_gaps():
    """
    Runs on schedule.
    Finds contacts you haven't interacted with recently.
    Sends reminder if needed.
    """

    print("Running relationship gap scan...")

    db = SessionLocal()

    try:
        contacts = db.query(Contact).all()

        for contact in contacts:
            print(f"Checking contact: {contact.name}")

            last_conversation = (
                db.query(Conversation)
                .filter(Conversation.phone_number == contact.phone_number)
                .order_by(Conversation.timestamp.desc())
                .first()
            )

            if not last_conversation:
                print("No conversation found.")
                continue

            days_since_last = (datetime.utcnow() - last_conversation.timestamp).days

            # TEMP: force test
            if days_since_last >= 0:
                message = f"You haven't talked to {contact.name} in {days_since_last} days."

                print("Sending reminder:", message)

                send_sms(
                    to_number="14166971728",  # your number
                    message=message
                )

    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_relationship_gaps, "interval", hours=5)
    scheduler.start()