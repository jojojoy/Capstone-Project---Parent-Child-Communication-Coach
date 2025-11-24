import os
import asyncio
from google import genai

MODEL_ID = "gemini-2.0-flash-001"


def get_client() -> genai.Client:
    """Initialize a Gemini client using the GOOGLE_API_KEY environment variable."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Please configure it before running."
        )
    return genai.Client(api_key=api_key)


async def run_once(child_message: str, child_age: int) -> str:
    """Lightweight version: emotion + needs analysis only."""
    client = get_client()

    prompt = f"""
You are a gentle, emotionally intelligent parenting coach.

A parent comes to you with this situation:

- Child's age: {child_age}
- Child's message: "{child_message}"

Please:
1. Explain the child's likely emotions.
2. Identify the child's underlying needs (2–4 items).
3. Keep the answer short (1–2 paragraphs + a bullet list).

Respond in clear English.
"""

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
    )
    return (response.text or "").strip()


async def run_full(child_message: str, child_age: int) -> str:
    """Full pipeline: analysis + 3 responses + coaching tips."""
    client = get_client()

    prompt = f"""
You are an AI "Parent–Child Communication Coach".

A parent comes to you with the following situation:

- Child's age: {child_age}
- Child's message: "{child_message}"

Produce a structured response with **three sections**:

### 1. Emotion & Needs Analysis
- Describe the child’s likely primary and secondary emotions.
- Identify 2–4 key underlying needs (e.g., autonomy, fun/play, competence, connection).
- Keep it concise (1–2 short paragraphs + a bullet list).

### 2. Suggested Parent Responses (3 options)
Provide exactly **three** example parent responses that:
- Validate the child's feelings.
- Avoid lecturing or blaming.
- Maintain boundaries if needed (e.g., bedtime still happens).

Format:
1. "..."
2. "..."
3. "..."

### 3. Coaching Tips for the Parent
Provide 4–6 concise bullet points explaining:
- Why the responses help de-escalate the situation.
- Common pitfalls to avoid.
- How to adjust tone for a {child_age}-year-old child.

Write in clear, simple English for stressed parents.
"""

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
    )
    return (response.text or "").strip()


def main() -> None:
    """Command-line entry point for local/Kaggle testing."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("⚠ GOOGLE_API_KEY is not set.\n")

    print("Parent–Child Communication Coach (full demo)\n")

    age_str = input("Child's age (e.g., 7 or 15): ").strip() or "12"
    try:
        age = int(age_str)
    except ValueError:
        age = 12

    print("\nPaste the child's message, then press Enter:\n")
    child_msg = input("> ")

    result = asyncio.run(run_full(child_msg, age))

    print("\n" + "=" * 80 + "\n")
    print(result)
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
