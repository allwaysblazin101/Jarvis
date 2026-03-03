import os
from database.connection import SessionLocal
from models.contact import Contact


def normalize_phone(phone: str) -> str:
    """Standardize phone format for matching."""
    if not phone:
        return ""

    return (
        phone.strip()
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
        .replace("+", "")
    )


def is_contact_allowed(phone_number: str) -> bool:
    """
    MVP Permission + Learning Mode

    Features:
    ✅ Allow all numbers (MVP design)
    ✅ Auto-create unknown contacts
    ✅ Track communication frequency
    """

    db = SessionLocal()

    try:
        normalized_number = normalize_phone(phone_number)

        contact = db.query(Contact).filter(
            Contact.phone_number == normalized_number
        ).first()

        # -----------------------------
        # Auto Learn New Contacts
        # -----------------------------
        if not contact:
            contact = Contact(
                name="Unknown",
                phone_number=normalized_number,
                relationship_type="unknown",
                importance_score=0.5,
                communication_frequency=1.0
            )

            db.add(contact)

        else:
            # Increase communication frequency (learning signal)
            contact.communication_frequency += 1

        db.commit()

        return True

    except Exception as e:
        print("Permission service error:", e)
        return True  # Fail open for MVP testing

    finally:
        db.close()


__all__ = ["is_contact_allowed", "normalize_phone"]
