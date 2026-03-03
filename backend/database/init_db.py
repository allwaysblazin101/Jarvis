from database.connection import Base, engine

def init_db():

    print("Creating database tables...")

    import models.contact
    import models.conversation
    import models.cognitive_state
    import models.pending_suggestion
    import models.contact_permission
    import models.reinforcement_memory
    import models.decision_memory
    import models.behavior
    import models.behavior_feedback
    import models.personality
    import models.social_memory
    import models.social_priority
    import models.user

    print("Tables detected:")
    for table in Base.metadata.tables:
        print(" →", table)

    Base.metadata.create_all(bind=engine)

    print("✅ Database ready")