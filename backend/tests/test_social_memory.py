import pytest
import asyncio
from services.ai_service import generate_ai_reply


@pytest.mark.asyncio
async def test_social_memory_flow():

    reply1 = await generate_ai_reply(
        message="Hey",
        phone_number="+TEST_SOCIAL"
    )

    reply2 = await generate_ai_reply(
        message="How are you?",
        phone_number="+TEST_SOCIAL"
    )

    assert reply1 is not None
    assert reply2 is not None
