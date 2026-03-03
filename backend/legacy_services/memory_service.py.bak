from database.connection import SessionLocal
from models.conversation import Conversation
from services.profile_learning_service import learn_user_profile_fact
from services.cognitive_memory_service import update_cognitive_memory
from services.feedback_learning_service import process_feedback_and_update_trust


# =========================================================
# Conversation Memory
# =========================================================

def get_recent_context(phone_number: str, limit: int = 5):

    db = SessionLocal()

    conversations = (
        db.query(Conversation)
        .filter(Conversation.phone_number == phone_number)
        .order_by(Conversation.timestamp.desc())
        .limit(limit)
        .all()
    )

    db.close()

    context_text = ""

    for conv in reversed(conversations):
        context_text += f"User: {conv.user_message}\n"
        context_text += f"AI: {conv.ai_response}\n"

    return context_text


# =========================================================
# Master Memory Learning Brain ⭐
# =========================================================

def learn_from_message(phone_number: str, message: str, tone_score: float):

    # Profile knowledge learning
    learn_user_profile_fact(phone_number, message)

    # Cognitive state learning
    update_cognitive_memory(
        phone_number=phone_number,
        tone_score=tone_score,
        message_length=len(message)
    )

    # Feedback reward learning
    feedback_keywords = ["good", "helpful", "thanks", "wrong", "bad"]

    if any(word in message.lower() for word in feedback_keywords):
        process_feedback_and_update_trust(phone_number)


# =========================================================
# Memory Prompt Context Builder
# =========================================================

def build_memory_prompt_context(phone_number: str):

    context = get_recent_context(phone_number)

    return f"""
Conversation History:
{context}
"""