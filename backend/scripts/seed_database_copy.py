print("Loading models...")

from models.contact import Contact
from models.conversation import Conversation
from models.cognitive_state import CognitiveState
from models.pending_suggestion import PendingSuggestion
from models.contact_permission import ContactPermission

from database.connection import Base, engine, SessionLocal


def seed_system():
    print("Dropping tables...")
    Base.metadata.drop_all(bind=engine)

    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    print("Seeding contacts...")

    db = SessionLocal()

    contacts = [
        {
            "name": "Mom",
            "phone_number": "+16476289395",
            "relationship_type": "family",
            "importance_score": 1.0
        },
        {
            "name": "Bigs",
            "phone_number": "+17058160166",
            "relationship_type": "friend",
            "importance_score": 0.9
        }
    ]

    for c in contacts:
        db.add(Contact(
            name=c["name"],
            phone_number=c["phone_number"],
            relationship_type=c["relationship_type"],
            importance_score=c["importance_score"],
            communication_frequency=0.0
        ))

    db.commit()
    db.close()

    print("✅ Database seeded successfully")