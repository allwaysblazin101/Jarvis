print("Loading models...")

from database.connection import Base, engine, SessionLocal
from models.contact import Contact


def seed_system():
    print("Creating database tables if not exist...")

    # Only create tables (NO DROPPING)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    print("Checking existing data...")

    # Seed only if database is empty
    if db.query(Contact).first():
        print("Database already seeded — skipping")
        db.close()
        return

    print("Seeding contacts...")

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


if __name__ == "__main__":
    seed_system()