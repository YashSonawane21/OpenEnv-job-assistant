"""Resume grader with rubric scoring and anti-gaming checks."""

from __future__ import annotations

import re
from collections import Counter


SKILL_GROUPS = {
    "python": {"python", "fastapi", "flask", "django", "pandas", "numpy"},
    "react": {"react", "javascript", "typescript", "frontend", "redux", "next.js", "nextjs"},
    "data": {"sql", "database", "postgres", "mysql", "etl", "analytics"},
    "delivery": {"project", "delivered", "launched", "impact", "improved", "led", "optimized"},
}


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z0-9+.#-]*", text.lower())


def _stuffing_penalty(text: str) -> tuple[float, bool]:
    tokens = _tokens(text)
    if len(tokens) < 20:
        return 0.0, False

    top_count = Counter(tokens).most_common(1)[0][1]
    ratio = top_count / max(1, len(tokens))
    if top_count >= 6 and ratio >= 0.12:
        return min(0.15, round((ratio - 0.12) * 1.5, 3)), True
    return 0.0, False


def evaluate_resume(resume: str, job_description: str = "") -> dict:
    text = (resume or "").strip()
    if not text:
        return {
            "score": 0.0,
            "breakdown": [],
            "strengths": [],
            "improvements": ["Add a resume summary and core technical skills relevant to the role."],
            "penalties": [],
            "quality_flags": {"empty_submission": True, "keyword_stuffing": False},
        }

    lower = text.lower()
    jd_lower = (job_description or "").lower()
    breakdown = []
    strengths: list[str] = []
    improvements: list[str] = []
    penalties: list[str] = []
    score = 0.0

    matched_groups = 0
    for group, keywords in SKILL_GROUPS.items():
        matched = any(word in lower for word in keywords)
        points = 0.18 if matched else 0.0
        score += points
        matched_groups += int(matched)
        breakdown.append(
            {
                "criterion": f"Skill coverage: {group}",
                "score": round(points, 3),
                "max_score": 0.18,
                "met": matched,
            }
        )

    if matched_groups >= 3:
        strengths.append("Resume shows broad skill coverage across engineering competencies.")
    else:
        improvements.append("Add more concrete skills (backend, frontend, data, and delivery impact).")

    if jd_lower:
        jd_keywords = [w for w in _tokens(jd_lower) if len(w) > 3]
        unique_matches = len({kw for kw in jd_keywords if kw in lower})
        context_score = min(0.2, unique_matches * 0.02)
        score += context_score
        breakdown.append(
            {
                "criterion": "Job description alignment",
                "score": round(context_score, 3),
                "max_score": 0.2,
                "met": context_score >= 0.1,
            }
        )
        if context_score >= 0.1:
            strengths.append("Resume is aligned with terms found in the job description.")
        else:
            improvements.append("Mirror more role-specific keywords from the job description.")
    else:
        breakdown.append(
            {
                "criterion": "Job description alignment",
                "score": 0.08,
                "max_score": 0.2,
                "met": False,
            }
        )
        score += 0.08

    token_count = len(_tokens(text))
    structure_score = 0.18 if 45 <= token_count <= 350 else (0.1 if token_count >= 25 else 0.0)
    score += structure_score
    breakdown.append(
        {
            "criterion": "Content depth and structure",
            "score": round(structure_score, 3),
            "max_score": 0.18,
            "met": structure_score >= 0.1,
        }
    )

    if structure_score < 0.1:
        improvements.append("Add measurable achievements and role-specific bullet points.")

    penalty, stuffing = _stuffing_penalty(text)
    if penalty > 0:
        score -= penalty
        penalties.append("Detected repeated keyword usage; reduce keyword stuffing and add meaningful context.")

    return {
        "score": round(max(0.0, min(score, 1.0)), 4),
        "breakdown": breakdown,
        "strengths": strengths,
        "improvements": improvements,
        "penalties": penalties,
        "quality_flags": {
            "empty_submission": False,
            "keyword_stuffing": stuffing,
            "very_short": token_count < 25,
        },
    }


def grade_resume(resume: str, job_description: str) -> float:
    return evaluate_resume(resume, job_description)["score"]
