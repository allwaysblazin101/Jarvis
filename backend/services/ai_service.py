import os
from typing import List

from openai import AsyncOpenAI

from services.tone_service import detect_tone
from services.phone_utils import normalize_phone

from services.memory_brain.master_memory_engine import (
    master_learn_from_message,
    build_master_prompt_context
)

from services.learning_orchestrator import unified_learning_cycle
from services.planning_engine import generate_basic_plan
from services.financial_intelligence_engine import generate_financial_guardrail
from services.action_execution_engine import execute_action_stub

from services.intelligence_perception_engine import (
    analyze_for_planning,
    detect_financial_intent
)

from services.life_optimizer_engine import generate_life_suggestion
from services.proactive_brain.proactive_foresight_engine import (
    predict_user_future_needs
)

from services.cognition_state import cognition, update_cognition_flags


client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

tone_score_map = {u
    "positive": 0.82,
    "happy": 0.88,
    "excited": 0.92,
    "joyful": 0.90,
    "neutral": 0.50,
    "negative": 0.18,
    "sad": 0.22,
    "angry": 0.10,
    "frustrated": 0.15,
}


system_prompt = """
You are AI Copilot — a sovereign personal AGI assistant.

Rules:
1. Only use explicit memory context.
2. Never hallucinate identity facts.
3. Stay emotionally grounded.
4. Be concise unless user asks for detail.
5. Protect user autonomy.
"""


# =====================================================
# MAIN REPLY ENGINE
# =====================================================

async def generate_ai_reply(phone_number: str, message: str) -> str:

    if not message or not message.strip():
        return "I'm here. What's up?"

    phone_number = normalize_phone(phone_number)

    tone = detect_tone(message)
    tone_score = tone_score_map.get(tone.lower(), 0.5)

    # Update cognition perception flags
    update_cognition_flags(message)

    # -----------------------------
    # Cognitive Guidance Layer
    # -----------------------------

    planning = analyze_for_planning(message)
    financial = detect_financial_intent(message)

    cognitive_guidance = []

    if planning:
        cognitive_guidance.append(
            generate_life_suggestion(message)
        )
        cognitive_guidance.append(
            generate_basic_plan(message)
        )

    if financial:
        cognitive_guidance.append(
            generate_financial_guardrail(message)
        )

    future_predictions = predict_user_future_needs(message)
    cognitive_guidance.extend(future_predictions)

    cognitive_guidance_text = "\n".join(cognitive_guidance)

    # -----------------------------
    # Memory Context
    # -----------------------------

    memory_context = build_master_prompt_context(
        phone_number=phone_number,
        limit=15
    )

    # -----------------------------
    # Prompt Construction
    # -----------------------------

    user_prompt = f"""
Memory Context:
{memory_context}

User Message:
{message}

Life Guidance:
{cognitive_guidance_text}

Respond naturally.
"""

    # -----------------------------
    # LLM Reply Generation
    # -----------------------------

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=350,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        ai_reply = response.choices[0].message.content.strip()

    except Exception as e:
        print("OpenAI error:", e)
        ai_reply = "I'm having trouble thinking right now…"

    # -----------------------------
    # Learning Loop
    # -----------------------------

    try:
        await master_learn_from_message(
            phone_number=phone_number,
            message=message,
            ai_reply=ai_reply,
            tone_score=tone_score,
            openai_client=client
        )

    except Exception as e:
        print("Final learn error:", e)

    return ai_reply


# =====================================================
# Suggestions Engine
# =====================================================

async def generate_reply_suggestions(
    phone_number: str,
    message: str
) -> List[str]:

    if not message:
        return ["Hey", "Tell me more", "I'm listening"]

    phone_number = normalize_phone(phone_number)

    memory_context = build_master_prompt_context(
        phone_number=phone_number,
        limit=12
    )

    prompt = f"""
Generate 3 natural short replies.

Context:
{memory_context}

Message:
{message}

Return 3 lines only.
"""

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.8,
            max_tokens=120,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content.strip()

        suggestions = [
            line.strip("-•*0123456789. ")
            for line in text.split("\n")
            if line.strip()
        ]

        return suggestions[:3]

    except Exception as e:
        print("Suggestion error:", e)
        return ["Okay", "Tell me more", "Got it"]