"""
Parent–Child Communication Coach agent, built with Google ADK.

Pipeline (SequentialAgent):
  1. EmotionAnalyzerAgent   -> output_key="emotion_summary"
  2. ResponseGeneratorAgent -> output_key="parent_responses"
  3. CoachingTipsAgent      -> uses both emotion_summary & parent_responses

This file is meant to be used as the root agent for ADK
(i.e. `root_agent` must be defined).
"""

from typing import List

from google.adk.agents import LlmAgent, SequentialAgent

GEMINI_MODEL = "gemini-2.0-flash"


# ---------------------------------------------------------------------------
# Custom tool: simple, rule-based regulation activity suggester
# ---------------------------------------------------------------------------

def suggest_regulation_activities(age: int) -> List[str]:
    """
    Return a few age-appropriate self-regulation or connection activities.

    This is a plain Python function used as a **custom tool** by the
    CoachingTipsAgent to enrich suggestions without another LLM call.
    """
    if age <= 8:
        return [
            "Draw or color feelings together for 5–10 minutes.",
            "Do a short breathing game: smell the flower, blow out the candle.",
            "Read a calm bedtime story while sitting close.",
        ]
    if age <= 12:
        return [
            "Take a short walk together and talk about the day.",
            "Do 5 slow breaths together, counting 1–5 on each exhale.",
            "Play a quick, silly game to release tension before talking.",
        ]
    # teens
    return [
        "Offer a hot drink and let them talk without interruption.",
        "Suggest a solo reset (shower, music, quiet time) before the conversation.",
        "Go for a drive or walk side-by-side to make talking feel less intense.",
    ]


# ---------------------------------------------------------------------------
# 1) Emotion Analyzer Agent
# ---------------------------------------------------------------------------

emotion_agent = LlmAgent(
    name="EmotionAnalyzerAgent",
    model=GEMINI_MODEL,
    description=(
        "Analyzes the child's message and extracts emotion, intensity, "
        "and underlying needs in a short, structured summary."
    ),
    instruction=(
        "You are an emotion and needs analyst for parent–child conversations.\n\n"
        "Given the child's message and any brief context from the parent, "
        "identify:\n"
        "  - primary emotions (e.g., frustrated, anxious, angry, sad, ashamed)\n"
        "  - secondary emotions if relevant\n"
        "  - 2–3 underlying needs (e.g., autonomy, space, competence, "
        "    belonging, safety, fairness)\n"
        "  - what might be *really* going on beneath the words\n\n"
        "Output a concise paragraph plus a short bullet list. "
        "This is for the parent only; never blame the child or the parent."
    ),
    # The text this agent generates will be stored in state['emotion_summary']
    output_key="emotion_summary",
)

# ---------------------------------------------------------------------------
# 2) Response Generator Agent
# ---------------------------------------------------------------------------

response_agent = LlmAgent(
    name="ResponseGeneratorAgent",
    model=GEMINI_MODEL,
    description=(
        "Generates 3 empathetic parent replies, using the emotion summary "
        "from the previous step."
    ),
    instruction=(
        "You are a gentle, emotionally attuned parenting coach.\n\n"
        "You have access to an emotion summary in {{ emotion_summary }}.\n"
        "Using that, generate **three** short parent responses that:\n"
        "  - start by validating the child's feelings\n"
        "  - stay calm and non-defensive\n"
        "  - avoid lectures, threats, or shaming\n"
        "  - keep the door open for future conversation\n\n"
        "Format your answer as:\n"
        "1. <first response>\n"
        "2. <second response>\n"
        "3. <third response>\n"
        "Keep each response to 1–2 sentences and write in natural, everyday "
        "language a caring parent might actually say."
    ),
    output_key="parent_responses",
)

# ---------------------------------------------------------------------------
# 3) Coaching Tips Agent (uses tool + previous state)
# ---------------------------------------------------------------------------

coaching_agent = LlmAgent(
    name="CoachingTipsAgent",
    model=GEMINI_MODEL,
    description=(
        "Provides coaching guidance to the parent, using emotion summary, "
        "candidate responses, and a regulation-activities tool."
    ),
    instruction=(
        "You are an experienced parenting coach.\n\n"
        "Context you can use:\n"
        "- Emotion summary: {{ emotion_summary }}\n"
        "- Candidate parent responses: {{ parent_responses }}\n\n"
        "The user will also tell you the approximate age of the child. "
        "You can call the `suggest_regulation_activities` tool to propose "
        "specific calming or co-regulation ideas.\n\n"
        "Your output should have three sections in Markdown:\n"
        "### How your child might be feeling\n"
        "Explain in 3–5 sentences what might be happening emotionally for "
        "the child, in a non-judgmental way.\n\n"
        "### How you can respond\n"
        "Briefly comment on the three suggested responses, and highlight "
        "what to prioritize (e.g., validation, timing, body language).\n\n"
        "### Practical tips\n"
        "Use the regulation-activities tool if helpful, and summarize "
        "3–5 concrete actions the parent can take in the next 24 hours.\n"
        "Keep the tone warm, encouraging, and shame-free."
    ),
    tools=[suggest_regulation_activities],
)

# ---------------------------------------------------------------------------
# Root Agent: Sequential pipeline
# ---------------------------------------------------------------------------

root_agent = SequentialAgent(
    name="ParentChildCommunicationCoach",
    sub_agents=[emotion_agent, response_agent, coaching_agent],
    description=(
        "A 3-step pipeline that analyzes the child's emotions, suggests "
        "empathetic parent responses, and gives coaching tips."
    ),
)
