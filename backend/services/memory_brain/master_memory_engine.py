import json
from datetime import datetime
from typing import List, Dict, Optional

from sqlalchemy.orm import Session
from sqlalchemy import desc

from database.connection import SessionLocal
from models.conversation import Conversation
from models.user_profile_memory import UserProfileMemory
from models.cognitive_state import CognitiveState


async def extract_facts_with_llm(
    message: str,
    ai_reply: str,
    context_snippet: str,
    openai_client
) -> List[Dict]:

    prompt = f"""
Extract ONLY explicit personal facts.

Return JSON only.

{{
 "facts":[]
}}

Message:
{message}

Reply:
{ai_reply}

Context:
{context_snippet}
"""

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()
        parsed = json.loads(raw)

        return parsed.get("facts", [])[:3]

    except:
        return []


def upsert_identity_memory(
    db: Session,
    phone_number: str,
    key: str,
    value: str,
    confidence: float
):

    if not key or not value:
        return

    existing = db.query(UserProfileMemory).filter(
        UserProfileMemory.phone_number == phone_number,
        UserProfileMemory.knowledge_key == key
    ).first()

    now = datetime.utcnow()

    if existing:
        if confidence > existing.confidence:
            existing.knowledge_value = value
            existing.confidence = confidence
            existing.timestamp = now
    else:
        db.add(UserProfileMemory(
            phone_number=phone_number,
            knowledge_key=key,
            knowledge_value=value,
            confidence=confidence,
            timestamp=now
        ))


async def master_learn_from_message(
    phone_number: str,
    message: str,
    ai_reply: Optional[str],
    tone_score: float,
    openai_client=None
):

    db = SessionLocal()

    try:
        db.add(
            Conversation(
                phone_number=phone_number,
                user_message=message,
                ai_response=ai_reply or "[no reply]",
                timestamp=datetime.utcnow()
            )
        )

        state = db.query(CognitiveState).filter(
            CognitiveState.phone_number == phone_number
        ).first()

        if not state:
            state = CognitiveState(
                phone_number=phone_number,
                trust_score=0.5,
                friendship_score=0.5
            )
            db.add(state)

        state.trust_score = min(
            1.0,
            max(0.1, state.trust_score + (tone_score - 0.5) * 0.08)
        )

        state.friendship_score = min(
            1.0,
            state.friendship_score + (len(message) / 12000)
        )

        if openai_client and ai_reply:

            context_snippet = build_master_prompt_context(phone_number)

            facts = await extract_facts_with_llm(
                message,
                ai_reply,
                context_snippet,
                openai_client
            )

            for fact in facts:
                if fact.get("confidence", 0) >= 0.5:
                    upsert_identity_memory(
                        db,
                        phone_number,
                        fact.get("key"),
                        fact.get("value"),
                        fact.get("confidence", 0.5)
                    )

        db.commit()

    except Exception as e:
        db.rollback()
        print("Memory learning error:", e)

    finally:
        db.close()


def build_master_prompt_context(phone_number: str, limit: int = 12):

    db = SessionLocal()

    try:
        facts = db.query(UserProfileMemory).filter(
            UserProfileMemory.phone_number == phone_number,
            UserProfileMemory.confidence >= 0.7
        ).order_by(desc(UserProfileMemory.confidence)).limit(limit).all()

        convs = db.query(Conversation).filter(
            Conversation.phone_number == phone_number
        ).order_by(desc(Conversation.timestamp)).limit(limit).all()

        parts = []

        if facts:
            parts.append("KNOWN USER FACTS:")
            for f in facts:
                parts.append(
                    f"• {f.knowledge_key}: {f.knowledge_value}"
                )

        parts.append("\nRECENT CONVERSATION:")
        for c in reversed(convs):
            parts.append(f"User: {c.user_message}")
            if c.ai_response:
                parts.append(f"AI: {c.ai_response}")
            parts.append("---")

        return "\n".join(parts)

    finally:
        db.close()