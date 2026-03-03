from services.ai_service import generate_ai_reply
import asyncio


test_messages = [
    "Hey",
    "How are you?",
    "Are you free later?",
    "Just checking in",
    "What are you doing?"
]


async def run_test():

    print("Starting AI flow test...")

    for msg in test_messages:

        print("\nTesting message:", msg)

        reply = await generate_ai_reply(
            message=msg,
            phone_number="+TEST_NUMBER"
        )

        print("AI Reply:", reply)


if __name__ == "__main__":
    asyncio.run(run_test())