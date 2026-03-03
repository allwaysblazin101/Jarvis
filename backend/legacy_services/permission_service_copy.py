from database.connection import SessionLocal
from models.contact import Contact


def normalize_phone(phone: str) -> str:
    if not phone:
        return ""

    return (
        phone.strip()
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )


def is_contact_allowed(phone_number: str) -> bool:
    """
    MVP mode:
    Allow all numbers.
    Auto-create contact if unknown.
    """

    db = SessionLocal()

    try:
        normalized_number = normalize_phone(phone_number)

        contact = db.query(Contact).filter(
            Contact.phone_number == normalized_number
        ).first()

        # If contact does not exist → auto-create it
        if not contact:
            new_contact = Contact(
                name="Unknown",
                phone_number=normalized_number,
                relationship_type="unknown",
                importance_score=0.5,
                communication_frequency=0.0
            )
            db.add(new_contact)
            db.commit()

        return True

    finally:
        db.close()