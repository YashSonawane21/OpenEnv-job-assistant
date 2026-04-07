"""Interview preparation grader with STAR, depth, and anti-gaming checks."""

from __future__ import annotations

import re
from collections import Counter


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z0-9'-]*", text.lower())


def _stuffing_penalty(text: str) -> tuple[float, bool]:
    tokens = _tokens(text)
    if len(tokens) < 35:
        return 0.0, False
    top_count = Counter(tokens).most_common(1)[0][1]
    ratio = top_count / max(1, len(tokens))
    if top_count >= 7 and ratio >= 0.1:
        return min(0.12, round((ratio - 0.1) * 1.4, 3)), True
    return 0.0, False


def evaluate_interview_prep(preparation_notes: str, job_description: str = "") -> dict:
    text = (preparation_notes or "").strip()
    if not text:
        return {
            "score": 0.0,
            "breakdown": [],
            "strengths": [],
            "improvements": ["Prepare STAR responses and technical examples tailored to the role."],
            "penalties": [],
            "quality_flags": {"empty_submission": True, "keyword_stuffing": False},
        }

    lower = text.lower()
    jd_lower = (job_description or "").lower()
    score = 0.0
    breakdown = []
    strengths: list[str] = []
    improvements: list[str] = []
    penalties: list[str] = []

    star_terms = ["situation", "task", "action", "result"]
    star_count = sum(1 for term in star_terms if term in lower)
    star_score = min(0.3, star_count * 0.075)
    score += star_score
    breakdown.append({"criterion": "STAR structure", "score": round(star_score, 3), "max_score": 0.3, "met": star_count >= 3})

    technical = any(
        k in lower
        for k in [
            "algorithm",
            "system design",
            "api",
            "database",
            "scalability",
            "latency",
            "optimization",
            "testing",
            "debugging",
        ]
    )
    technical_score = 0.2 if technical else 0.0
    score += technical_score
    breakdown.append({"criterion": "Technical depth", "score": technical_score, "max_score": 0.2, "met": technical})

    problem_solving = any(
        k in lower for k in ["approach", "trade-off", "decision", "analyze", "evaluate", "hypothesis", "measure"]
    )
    problem_score = 0.18 if problem_solving else 0.0
    score += problem_score
    breakdown.append({"criterion": "Problem-solving clarity", "score": problem_score, "max_score": 0.18, "met": problem_solving})

    if jd_lower:
        jd_keywords = [w for w in _tokens(jd_lower) if len(w) > 3]
        matches = len({kw for kw in jd_keywords if kw in lower})
        research_score = min(0.17, matches * 0.02)
    else:
        research_score = 0.08
    score += research_score
    breakdown.append({"criterion": "Role/company research", "score": round(research_score, 3), "max_score": 0.17, "met": research_score >= 0.08})

    token_count = len(_tokens(text))
    practice_mentions = any(k in lower for k in ["practice", "mock interview", "rehearse", "timed", "feedback"])
    practice_score = 0.15 if practice_mentions and token_count >= 70 else (0.08 if token_count >= 70 else 0.03)
    score += practice_score
    breakdown.append({"criterion": "Preparation depth", "score": practice_score, "max_score": 0.15, "met": practice_score >= 0.08})

    if star_count >= 3:
        strengths.append("Preparation notes follow a strong STAR-style response structure.")
    if technical and problem_solving:
        strengths.append("Notes balance technical detail with reasoning process.")

    if star_count < 3:
        improvements.append("Write responses in full STAR format: Situation, Task, Action, Result.")
    if not technical:
        improvements.append("Add one technical deep-dive example with metrics or outcomes.")
    if research_score < 0.08:
        improvements.append("Include role-specific research points linked to the company context.")

    penalty, stuffing = _stuffing_penalty(text)
    if penalty > 0:
        score -= penalty
        penalties.append("Detected repetitive phrasing; replace repeated words with concrete examples.")

    return {
        "score": round(max(0.0, min(score, 1.0)), 4),
        "breakdown": breakdown,
        "strengths": strengths,
        "improvements": improvements,
        "penalties": penalties,
        "quality_flags": {
            "empty_submission": False,
            "keyword_stuffing": stuffing,
            "very_short": token_count < 50,
        },
    }


def grade_interview_prep(preparation_notes: str, job_description: str = "") -> float:
    return evaluate_interview_prep(preparation_notes, job_description)["score"]
