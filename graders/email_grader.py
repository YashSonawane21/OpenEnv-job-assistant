"""Email grader with rubric and anti-spam checks."""

from __future__ import annotations

import re
from collections import Counter


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z0-9'-]*", text.lower())


def _stuffing_penalty(text: str) -> tuple[float, bool]:
    tokens = _tokens(text)
    if len(tokens) < 15:
        return 0.0, False
    top_count = Counter(tokens).most_common(1)[0][1]
    ratio = top_count / max(1, len(tokens))
    if top_count >= 5 and ratio >= 0.16:
        return min(0.12, round((ratio - 0.16) * 1.2, 3)), True
    return 0.0, False


def evaluate_email(email: str) -> dict:
    text = (email or "").strip()
    if not text:
        return {
            "score": 0.0,
            "breakdown": [],
            "strengths": [],
            "improvements": ["Add a professional greeting, intent, and a clear closing line."],
            "penalties": [],
            "quality_flags": {"empty_submission": True, "keyword_stuffing": False},
        }

    lower = text.lower()
    breakdown = []
    strengths: list[str] = []
    improvements: list[str] = []
    penalties: list[str] = []
    score = 0.0

    greeting = any(g in lower for g in ["hello", "dear", "hi ", "good morning", "good afternoon"])
    greeting_score = 0.2 if greeting else 0.0
    score += greeting_score
    breakdown.append({"criterion": "Professional greeting", "score": greeting_score, "max_score": 0.2, "met": greeting})

    intent = any(
        key in lower
        for key in ["interested", "excited", "apply", "opportunity", "position", "role", "contribute"]
    )
    intent_score = 0.3 if intent else 0.0
    score += intent_score
    breakdown.append({"criterion": "Clear intent", "score": intent_score, "max_score": 0.3, "met": intent})

    evidence = any(key in lower for key in ["experience", "built", "led", "delivered", "skills", "background", "impact"])
    evidence_score = 0.25 if evidence else 0.0
    score += evidence_score
    breakdown.append(
        {"criterion": "Relevant qualification evidence", "score": evidence_score, "max_score": 0.25, "met": evidence}
    )

    closing = any(key in lower for key in ["thank you", "thanks", "sincerely", "regards", "looking forward"])
    closing_score = 0.15 if closing else 0.0
    score += closing_score
    breakdown.append({"criterion": "Professional closing", "score": closing_score, "max_score": 0.15, "met": closing})

    token_count = len(_tokens(text))
    brevity_score = 0.1 if 30 <= token_count <= 160 else (0.05 if token_count >= 20 else 0.0)
    score += brevity_score
    breakdown.append({"criterion": "Length quality", "score": brevity_score, "max_score": 0.1, "met": brevity_score > 0.0})

    if greeting and intent:
        strengths.append("Email opens professionally and communicates clear interest.")
    if evidence:
        strengths.append("Email includes evidence of relevant experience.")

    if not greeting:
        improvements.append("Start with a professional greeting to improve tone.")
    if not evidence:
        improvements.append("Add one concise achievement to prove fit for the role.")
    if not closing:
        improvements.append("Close with a polite sign-off and thank-you.")

    penalty, stuffing = _stuffing_penalty(text)
    if penalty > 0:
        score -= penalty
        penalties.append("Repetition detected; reduce repeated terms and keep the message natural.")

    return {
        "score": round(max(0.0, min(score, 1.0)), 4),
        "breakdown": breakdown,
        "strengths": strengths,
        "improvements": improvements,
        "penalties": penalties,
        "quality_flags": {
            "empty_submission": False,
            "keyword_stuffing": stuffing,
            "very_short": token_count < 20,
        },
    }


def grade_email(email: str) -> float:
    return evaluate_email(email)["score"]
