from database.connection import SessionLocal
from models.user_profile_memory import UserProfileMemory


def store_long_term_goal(phone_number: str, goal_text: str):
    db = SessionLocal()

    db.add(
        UserProfileMemory(
            phone_number=phone_number,
            memory_type="long_term_goal",
            content=goal_text
        )
    )

    db.commit()
    db.close()


def get_long_term_goals(phone_number: str):
    db = SessionLocal()

    goals = db.query(UserProfileMemory).filter(
        UserProfileMemory.phone_number == phone_number,
        UserProfileMemory.memory_type == "long_term_goal"
    ).all()

    db.close()

    return [g.content for g in goals]
