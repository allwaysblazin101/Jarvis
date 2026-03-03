import pytest
import asyncio
from services.ai_service import generate_ai_reply


@pytest.mark.asyncio
async def test_emotional_support_response():

    sad_messages = [
        "I feel sad today",
        "Not having a good day",
        "Things are hard right now"
    ]

    for msg in sad_messages:

        reply = await generate_ai_reply(
            message=msg,
            phone_number="+TEST_NUMBER"
        )

        assert any(word in reply.lower() for word in [
            "sorry",
            "understand",
            "here",
            "support"
        ])
