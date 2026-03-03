import os
from datetime import datetime

from fastapi import APIRouter, Request, Form

from services.ai_service import generate_ai_reply, generate_reply_suggestions
from services.sms_service import send_sms
from services.permission_service import is_contact_allowed
from services.phone_utils import normalize_phone

from database.connection import SessionLocal
from models.conversation import Conversation

router = APIRouter()

# ------------------------------------------------
# ENV CONFIG
# ------------------------------------------------

OWNER_NUMBER = os.getenv("OWNER_NUMBER")

TWILIO_NUMBERS = {
    os.getenv("TWILIO_NUMBER_PRIMARY"),
    os.getenv("TWILIO_NUMBER_SECONDARY")
}

# Remove None values if env not set
TWILIO_NUMBERS = {n for n in TWILIO_NUMBERS if n}


# ------------------------------------------------
# WEBHOOK
# ------------------------------------------------

@router.post("/sms/webhook")
async def receive_sms(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...)
):

    message = Body.strip()
    from_number_raw = From

    if not message or not from_number_raw:
        return {"status": "invalid_request"}

    from_number = normalize_phone(from_number_raw)

    print(f"[SMS IN] From {from_number}: {message}")

    # ------------------------------------------------
    # SECURITY + VALIDATION LAYER
    # ------------------------------------------------

    if (
        from_number not in TWILIO_NUMBERS
        and from_number != OWNER_NUMBER
    ):
        print(f"[SMS] Blocked number: {from_number}")
        return {"status": "blocked"}

    # ------------------------------------------------
    # OWNER FULL AI MODE
    # ------------------------------------------------

    if from_number == OWNER_NUMBER:

        try:
            ai_reply = await generate_ai_reply(
                phone_number=from_number,
                message=message
            )

            send_sms(
                to_number=OWNER_NUMBER,
                message=ai_reply
            )

            print(f"[SMS] Full AI reply sent to owner: {ai_reply[:80]}...")

        except Exception as e:
            print(f"[Owner AI] Error: {e}")
            send_sms(
                to_number=OWNER_NUMBER,
                message="Sorry, something went wrong..."
            )

        return {"status": "owner_full_reply_sent"}

    # ------------------------------------------------
    # CONTACT REPLY SUGGESTION MODE
    # ------------------------------------------------

    db = SessionLocal()

    try:

        # Check for pending confirmation
        last_incoming = db.query(Conversation).filter(
            Conversation.phone_number == from_number,
            Conversation.ai_response.like("%pending_owner_confirmation%")
        ).order_by(Conversation.timestamp.desc()).first()

        # ------------------------------------------------
        # OWNER CONFIRMATION PATH
        # ------------------------------------------------

        if last_incoming and OWNER_NUMBER in message:

            choice = message.strip().lower()

            suggestions = last_incoming.ai_response.split("\n") if last_incoming.ai_response else []

            if choice in ["1", "2"]:
                idx = int(choice) - 1
                reply_to_send = suggestions[idx] if idx < len(suggestions) else "Got it!"
            else:
                reply_to_send = message

            send_sms(
                to_number=from_number,
                message=reply_to_send
            )

            last_incoming.ai_response = reply_to_send
            db.commit()

            return {"status": "confirmation_processed"}

        # ------------------------------------------------
        # NORMAL CONTACT → SEND SUGGESTIONS TO OWNER ONLY
        # ------------------------------------------------

        suggestions = await generate_reply_suggestions(
            phone_number=from_number,
            message=message
        )

        suggestions = suggestions[:2]

        suggestion_text = "AI Suggestions:\n" + "\n".join(
            f"{i+1}. {s}" for i, s in enumerate(suggestions)
        )

        owner_message = f"""
From {from_number}
{message}

{suggestion_text}

Reply with 1 or 2 (or type your own response)
"""

        send_sms(
            to_number=OWNER_NUMBER,
            message=owner_message
        )

        print(f"[SMS] Suggestions sent to owner")

        # Save pending state
        db.add(
            Conversation(
                phone_number=from_number,
                user_message=message,
                ai_response="[pending_owner_confirmation]\n" + "\n".join(suggestions),
                timestamp=datetime.utcnow()
            )
        )

        db.commit()

    except Exception as e:
        print(f"[SMS Suggestions] Error: {e}")
        send_sms(
            to_number=OWNER_NUMBER,
            message=f"From {from_number}:\n{message}\n\nError generating suggestions."
        )

    finally:
        db.close()

    return {"status": "suggestions_sent_to_owner"}