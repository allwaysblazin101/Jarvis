import pytest
import asyncio
from services.ai_service import generate_ai_reply


@pytest.mark.asyncio
async def test_basic_responses():

    messages = [
        "Hey",
        "How are you?",
        "Are you free later?"
    ]

    for msg in messages:
        reply = await generate_ai_reply(
            message=msg,
            phone_number="+TEST_NUMBER"
        )

        assert reply is not None
        assert isinstance(reply, str)
        assert len(reply) > 0
