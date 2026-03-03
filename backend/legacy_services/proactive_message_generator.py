import random

from services.memory_brain.master_memory_engine import build_master_prompt_context


def generate_checkin_message(phone_number: str, name_fallback: str = "friend") -> str:
    """
    Generates a simple, slightly personalized proactive check-in message.
    """
    context = build_master_prompt_context(phone_number, limit=6)

    # Improved name extraction (still basic, but safer)
    name = name_fallback
    if "name:" in context.lower():
        for line in context.split("\n"):
            if "name:" in line.lower():
                try:
                    name_part = line.split(":", 1)[1].strip()
                    if len(name_part) < 30 and name_part.isprintable():
                        name = name_part
                        break
                except:
                    pass

    # Tone-aware variants (very basic)
    options = [
        f"Hey {name}, just checking in — how's everything going? 😊",
        f"Hi {name}! Been a while — hope you're doing alright?",
        f"Hey {name}, thought of you — what's the latest with you?",
        f"Yo {name} 👋 Just popping in to say hi — how you holding up?",
        f"Hey {name}, hope your day's going well — any updates?"
    ]

    return random.choice(options)