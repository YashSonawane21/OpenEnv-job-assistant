"""
Interview Readiness Grader
Evaluates preparation for interviews:
- STAR method usage (Situation, Task, Action, Result)
- Technical knowledge indicators
- Problem-solving approach
- Communication clarity
Scores: 0.0 - 1.0
"""


def grade_interview_prep(preparation_notes: str, job_description: str = "") -> float:
    """
    Grade interview preparation based on quality of notes and readiness.
    
    Args:
        preparation_notes: Interview prep notes from candidate
        job_description: Job description context (optional)
    
    Returns:
        float: Score between 0.0 and 1.0
    """
    if not preparation_notes or len(preparation_notes.strip()) == 0:
        return 0.0

    score = 0.0
    notes_lower = preparation_notes.lower()

    # Check for STAR method structure (0.25)
    star_keywords = ["situation", "task", "action", "result", "challenge"]
    star_count = sum(1 for keyword in star_keywords if keyword in notes_lower)
    star_score = min((star_count / 3) * 0.25, 0.25)
    score += star_score

    # Check for technical knowledge (0.2)
    if any(tech in notes_lower for tech in [
        "algorithm", "data structure", "design pattern", "api", 
        "database", "query", "optimization", "scalability"
    ]):
        score += 0.2

    # Check for problem-solving approach (0.2)
    if any(approach in notes_lower for approach in [
        "solve", "approach", "solution", "strategy", "method", 
        "think", "analyze", "evaluate", "trade-off"
    ]):
        score += 0.2

    # Check for company/role research (0.15)
    if job_description and any(research in notes_lower for research in [
        "company", "mission", "product", "role", "team", "culture"
    ]):
        job_keywords = [kw.strip() for kw in job_description.split() if len(kw) > 3]
        matching = sum(1 for kw in job_keywords if kw.lower() in notes_lower)
        research_score = min((matching / 5) * 0.15, 0.15)
        score += research_score
    elif not job_description:
        score += 0.075  # Partial credit

    # Check for depth (0.1)
    if len(preparation_notes.strip()) > 100:
        score += 0.05
    if len(preparation_notes.strip()) > 300:
        score += 0.05

    # Check for practice/mock interview mention (0.1)
    if any(practice in notes_lower for practice in [
        "practice", "mock", "interview", "rehearse", "prepare", "simulate"
    ]):
        score += 0.1

    return min(score, 1.0)
