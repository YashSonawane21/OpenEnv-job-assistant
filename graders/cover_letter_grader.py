"""Cover letter grader with contextual relevance and anti-gaming checks."""

from __future__ import annotations

import re
from collections import Counter


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z0-9'-]*", text.lower())


def _stuffing_penalty(text: str) -> tuple[float, bool]:
    tokens = _tokens(text)
    if len(tokens) < 40:
        return 0.0, False
    top_count = Counter(tokens).most_common(1)[0][1]
    ratio = top_count / max(1, len(tokens))
    if top_count >= 8 and ratio >= 0.1:
        return min(0.12, round((ratio - 0.1) * 1.3, 3)), True
    return 0.0, False


def evaluate_cover_letter(cover_letter: str, job_description: str = "") -> dict:
    text = (cover_letter or "").strip()
    if not text:
        return {
            "score": 0.0,
            "breakdown": [],
            "strengths": [],
            "improvements": ["Write a role-specific cover letter with greeting, achievements, and closing."],
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

    greeting = any(g in lower for g in ["dear", "hello", "hiring manager", "to the hiring team"])
    greeting_score = 0.15 if greeting else 0.0
    score += greeting_score
    breakdown.append({"criterion": "Professional opening", "score": greeting_score, "max_score": 0.15, "met": greeting})

    experience = any(w in lower for w in ["experience", "achieved", "delivered", "led", "built", "improved", "impact"])
    experience_score = 0.25 if experience else 0.0
    score += experience_score
    breakdown.append({"criterion": "Evidence of achievements", "score": experience_score, "max_score": 0.25, "met": experience})

    if jd_lower:
        jd_keywords = [w for w in _tokens(jd_lower) if len(w) > 3]
        matches = len({kw for kw in jd_keywords if kw in lower})
        alignment_score = min(0.3, matches * 0.03)
    else:
        alignment_score = 0.12
    score += alignment_score
    breakdown.append(
        {
            "criterion": "Role alignment",
            "score": round(alignment_score, 3),
            "max_score": 0.3,
            "met": alignment_score >= 0.15,
        }
    )

    closing = any(w in lower for w in ["thank you", "sincerely", "regards", "looking forward", "would welcome"])
    closing_score = 0.15 if closing else 0.0
    score += closing_score
    breakdown.append({"criterion": "Closing and call to action", "score": closing_score, "max_score": 0.15, "met": closing})

    token_count = len(_tokens(text))
    depth_score = 0.15 if 90 <= token_count <= 380 else (0.08 if token_count >= 60 else 0.0)
    score += depth_score
    breakdown.append({"criterion": "Depth and clarity", "score": depth_score, "max_score": 0.15, "met": depth_score >= 0.08})

    if experience:
        strengths.append("Cover letter includes evidence-oriented language.")
    if alignment_score >= 0.15:
        strengths.append("Content is aligned with the target role.")

    if not greeting:
        improvements.append("Use a direct professional greeting to strengthen the opening.")
    if not experience:
        improvements.append("Include one or two measurable achievements from past work.")
    if alignment_score < 0.15:
        improvements.append("Reflect more terms from the job description to show fit.")
    if not closing:
        improvements.append("Add a clear call-to-action and polite close.")

    penalty, stuffing = _stuffing_penalty(text)
    if penalty > 0:
        score -= penalty
        penalties.append("Repeated terms detected; reduce keyword repetition and add concrete details.")

    return {
        "score": round(max(0.0, min(score, 1.0)), 4),
        "breakdown": breakdown,
        "strengths": strengths,
        "improvements": improvements,
        "penalties": penalties,
        "quality_flags": {
            "empty_submission": False,
            "keyword_stuffing": stuffing,
            "very_short": token_count < 60,
        },
    }


def grade_cover_letter(cover_letter: str, job_description: str = "") -> float:
    return evaluate_cover_letter(cover_letter, job_description)["score"]
