import asyncio

from app.agent.chat_agent2 import ask_agent


async def main():
    questions = [
        "List all students.",
        "List all courses.",
        "Enroll student with email ana@example.com in course 1.",
        "Get student 999."
    ]

    for q in questions:
        print(f"\nUSER: {q}")
        answer = await ask_agent(q)
        print(f"AGENT: {answer}")


if __name__ == "__main__":
    asyncio.run(main())