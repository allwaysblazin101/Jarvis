from database.connection import SessionLocal
from models.contact_permission import ContactPermission


# ----------------------------
# Social Cognition Intelligence
# ----------------------------

def update_social_relationship(phone_number, message_length=0, tone=None):

    db = SessionLocal()

    contact = db.query(ContactPermission).filter(
        ContactPermission.phone_number == phone_number
    ).first()

    if not contact:
        db.close()
        return

    # Relationship intelligence learning
    if message_length > 50:
        contact.priority_score = (contact.priority_score or 50) + 0.2

    if tone == "positive":
        contact.priority_score += 0.1

    if tone == "negative":
        contact.priority_score -= 0.1

    # Clamp values
    if contact.priority_score > 100:
        contact.priority_score = 100

    if contact.priority_score < 0:
        contact.priority_score = 0

    db.commit()
    db.close()


def get_social_context(phone_number):

    db = SessionLocal()

    contact = db.query(ContactPermission).filter(
        ContactPermission.phone_number == phone_number
    ).first()

    db.close()

    if not contact:
        return None

    return {
        "name": contact.name,
        "relationship_type": contact.relationship_type,
        "priority_score": contact.priority_score
    }
