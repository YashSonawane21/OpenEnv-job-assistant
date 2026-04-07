"""LinkedIn profile grader with completeness and credibility checks."""

from __future__ import annotations

import re
from collections import Counter


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z0-9+.#'-]*", text.lower())


def _stuffing_penalty(text: str) -> tuple[float, bool]:
    tokens = _tokens(text)
    if len(tokens) < 35:
        return 0.0, False
    top_count = Counter(tokens).most_common(1)[0][1]
    ratio = top_count / max(1, len(tokens))
    if top_count >= 7 and ratio >= 0.11:
        return min(0.1, round((ratio - 0.11) * 1.2, 3)), True
    return 0.0, False


def evaluate_linkedin_profile(profile_data: str) -> dict:
    text = (profile_data or "").strip()
    if not text:
        return {
            "score": 0.0,
            "breakdown": [],
            "strengths": [],
            "improvements": ["Add headline, summary, skills, and experience to improve profile completeness."],
            "penalties": [],
            "quality_flags": {"empty_submission": True, "keyword_stuffing": False},
        }

    lower = text.lower()
    score = 0.0
    breakdown = []
    strengths: list[str] = []
    improvements: list[str] = []
    penalties: list[str] = []

    photo = any(k in lower for k in ["photo", "headshot", "profile picture", "image"])
    photo_score = 0.1 if photo else 0.0
    score += photo_score
    breakdown.append({"criterion": "Professional photo mention", "score": photo_score, "max_score": 0.1, "met": photo})

    headline = any(
        k in lower
        for k in ["engineer", "developer", "analyst", "manager", "architect", "specialist", "lead", "senior"]
    )
    headline_score = 0.16 if headline else 0.0
    score += headline_score
    breakdown.append({"criterion": "Headline quality", "score": headline_score, "max_score": 0.16, "met": headline})

    token_count = len(_tokens(text))
    summary_score = 0.2 if token_count >= 80 else (0.1 if token_count >= 40 else 0.0)
    score += summary_score
    breakdown.append({"criterion": "Summary depth", "score": summary_score, "max_score": 0.2, "met": summary_score > 0.0})

    skills = any(
        k in lower
        for k in [
            "skills",
            "expertise",
            "technologies",
            "python",
            "java",
            "javascript",
            "react",
            "sql",
            "aws",
            "docker",
        ]
    )
    skills_score = 0.18 if skills else 0.0
    score += skills_score
    breakdown.append({"criterion": "Skills visibility", "score": skills_score, "max_score": 0.18, "met": skills})

    experience = any(
        k in lower for k in ["experience", "worked", "built", "led", "delivered", "project", "company", "years"]
    )
    experience_score = 0.18 if experience else 0.0
    score += experience_score
    breakdown.append(
        {"criterion": "Experience credibility", "score": experience_score, "max_score": 0.18, "met": experience}
    )

    contact = any(k in lower for k in ["contact", "email", "message", "reach out", "connect", "linkedin.com/in/"])
    contact_score = 0.1 if contact else 0.0
    score += contact_score
    breakdown.append({"criterion": "Contact and CTA", "score": contact_score, "max_score": 0.1, "met": contact})

    social_proof = any(k in lower for k in ["recommendation", "endorsement", "testimonial", "certification"])
    social_score = 0.08 if social_proof else 0.0
    score += social_score
    breakdown.append({"criterion": "Social proof", "score": social_score, "max_score": 0.08, "met": social_proof})

    if headline and skills and experience:
        strengths.append("Profile includes strong fundamentals: headline, skills, and experience.")
    if social_proof:
        strengths.append("Social proof signals professional credibility.")

    if not headline:
        improvements.append("Use a specific headline that includes your role and specialization.")
    if summary_score < 0.1:
        improvements.append("Expand your summary with value proposition, achievements, and focus areas.")
    if not contact:
        improvements.append("Add a contact call-to-action so recruiters can reach you quickly.")

    penalty, stuffing = _stuffing_penalty(text)
    if penalty > 0:
        score -= penalty
        penalties.append("Detected repetitive wording; diversify phrasing with concrete outcomes.")

    return {
        "score": round(max(0.0, min(score, 1.0)), 4),
        "breakdown": breakdown,
        "strengths": strengths,
        "improvements": improvements,
        "penalties": penalties,
        "quality_flags": {
            "empty_submission": False,
            "keyword_stuffing": stuffing,
            "very_short": token_count < 40,
        },
    }


def grade_linkedin_profile(profile_data: str) -> float:
    return evaluate_linkedin_profile(profile_data)["score"]
