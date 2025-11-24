"""
Simple CLI / script entrypoint to talk to the Parent–Child Communication Coach
agent defined in agent.py.

Usage (after setting GOOGLE_API_KEY in your environment):

    python main.py
"""

import asyncio
import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent  # import the SequentialAgent pipeline

APP_NAME = "parent_child_communication_coach"
USER_ID = "demo_parent"
SESSION_ID = "session_1"


async def setup_session_and_runner():
    """Create an in-memory session and a Runner bound to our root_agent."""
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    return runner


async def run_once(child_message: str, child_age: int) -> str:
    """
    Send one turn to the agent.

    We stuff the age into the text prompt for simplicity; the CoachingTipsAgent
    can also call the regulation-activities tool using this age.
    """
    runner = await setup_session_and_runner()

    prompt = (
        f"My child is about {child_age} years old. "
        f"This is what they said or how they acted:\n\n{child_message}\n\n"
        "Please help me understand their emotions and suggest how I can "
        "respond in a calm, empathetic way."
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    )

    events = runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content,
    )

    final_text = ""
    async for event in events:
        if event.is_final_response():
            # ADK wraps Gemini responses in Content/Part objects.
            final_text = event.content.parts[0].text or ""
            break

    return final_text


def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print(
            "⚠️  WARNING: GOOGLE_API_KEY is not set.\n"
            "    Set it before running this script so Gemini can be called."
        )

    print("Parent–Child Communication Coach (one-shot demo)\n")
    age_str = input("Child's age (e.g. 7 or 15): ").strip() or "12"
    try:
        age = int(age_str)
    except ValueError:
        age = 12

    print("\nPaste what your child said or did, then press Enter:\n")
    child_msg = input("> ")

    result = asyncio.run(run_once(child_msg, age))

    print("\n===== Agent Response =====\n")
    print(result)
    print("\n==========================\n")


if __name__ == "__main__":
    main()
