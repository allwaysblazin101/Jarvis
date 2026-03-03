from typing import Dict
from services.goal_memory_engine import store_long_term_goal


def analyze_for_planning(phone_number: str, message: str) -> Dict:

    message_lower = message.lower()

    planning_keywords = [
        "plan", "goal", "save", "budget",
        "improve", "build", "start", "fix",
        "schedule", "organize"
    ]

    requires_plan = any(word in message_lower for word in planning_keywords)

    if requires_plan:
        store_long_term_goal(phone_number, message)

    return {
        "requires_planning": requires_plan,
        "goal_detected": message if requires_plan else None
    }


def generate_basic_plan(goal_text: str) -> str:

    return f"""
Structured Plan:

1. Define measurable version of: {goal_text}
2. Set weekly milestone
3. Track daily behavior
4. Review monthly progress
"""
