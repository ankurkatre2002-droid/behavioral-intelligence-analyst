"""
Behavioral Intelligence Analyst — Agent Logic
Contains the Clarifier Agent and Analyst Agent as separate functions.
Uses Groq API with LLaMA 3.3 70B for inference.
"""

import os
import json
from groq import Groq

MODEL = "llama-3.3-70b-versatile"

# Lazy-initialized client (created on first call, after .env is loaded)
_client = None

def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    return _client

# ─── System Prompts ──────────────────────────────────────────────────────────

CLARIFIER_SYSTEM_PROMPT = """You are a behavioral analytics assistant. Your only job at this stage is to decide if the user's query contains enough information to perform a meaningful behavioral analysis.

A query is SUFFICIENT if it describes: some kind of user behavior (sessions, engagement, activity, purchases, logins etc), at least a rough sense of scale or pattern, and what the user wants to understand.

A query is VAGUE if it is missing all behavioral detail, for example "my users are dropping off" with no further context.

If SUFFICIENT: respond with exactly this JSON: {"sufficient": true}
If VAGUE: respond with exactly this JSON: {"sufficient": false, "question": "your single clarifying question here"}

Ask only one question. Make it specific and focused. Never ask multiple questions.
Always respond in valid JSON only. No preamble, no explanation."""

ANALYST_SYSTEM_PROMPT = """You are a senior behavioral intelligence analyst. You reason about user and customer behavior patterns the way a product scientist at a top tech company would.

When given a description of user behavior, you produce a structured analysis with these four sections:

**Behavioral Segments** — identify 2-4 distinct user groups based on the behavior described. Give each segment a name and a one-line behavioral profile.

**Risk Flags** — identify which segments or behaviors signal churn risk, disengagement, or decline. Be specific about what signal indicates the risk.

**Actionable Recommendations** — give exactly 3 concrete recommendations the person can act on immediately based on the behavioral patterns. Each recommendation should be one to two sentences.

**Follow-up Suggestion** — suggest one specific follow-up question the user might want to explore next, phrased as a question.

Keep your tone analytical but plain. No jargon. Write like you are briefing a smart product manager who wants clarity, not complexity."""


# ─── Agent Functions ─────────────────────────────────────────────────────────

def clarifier_agent(conversation_history: list) -> dict:
    """
    Evaluates whether the user's query has enough detail for behavioral analysis.

    Args:
        conversation_history: List of message dicts with 'role' and 'content' keys.

    Returns:
        dict with keys:
            - "sufficient": bool
            - "question": str or None
    """
    messages = [{"role": "system", "content": CLARIFIER_SYSTEM_PROMPT}] + conversation_history

    try:
        response = _get_client().chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.2,
            max_completion_tokens=256,
        )
        raw = response.choices[0].message.content.strip()

        # Parse JSON response
        result = json.loads(raw)
        return {
            "sufficient": result.get("sufficient", True),
            "question": result.get("question", None),
        }

    except (json.JSONDecodeError, KeyError, IndexError):
        # If parsing fails, default to treating the query as sufficient
        return {"sufficient": True, "question": None}

    except Exception:
        # On any API or unexpected error, default to sufficient
        return {"sufficient": True, "question": None}


def analyst_agent(conversation_history: list) -> str:
    """
    Produces a structured behavioral analysis from the user's query
    (and any clarification provided).

    Args:
        conversation_history: List of message dicts with 'role' and 'content' keys.

    Returns:
        Formatted analysis string.
    """
    messages = [{"role": "system", "content": ANALYST_SYSTEM_PROMPT}] + conversation_history

    try:
        response = _get_client().chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.4,
            max_completion_tokens=1500,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Analysis could not be completed. Error: {str(e)}"