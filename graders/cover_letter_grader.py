"""
Cover Letter Grader
Evaluates the quality of a cover letter based on:
- Professional tone
- Job-specific details
- Call-to-action
- Proper structure
Scores: 0.0 - 1.0
"""


def grade_cover_letter(cover_letter: str, job_description: str = "") -> float:
    """
    Grade a cover letter based on quality indicators.
    
    Args:
        cover_letter: The cover letter text
        job_description: Job description context (optional)
    
    Returns:
        float: Score between 0.0 and 1.0
    """
    if not cover_letter or len(cover_letter.strip()) == 0:
        return 0.0

    score = 0.0
    cover_letter_lower = cover_letter.lower()

    # Check for professional greeting (0.2)
    if any(greeting in cover_letter_lower for greeting in ["dear", "hello", "greetings"]):
        score += 0.2

    # Check for personal experience/skills (0.3)
    if any(keyword in cover_letter_lower for keyword in [
        "experience", "skilled", "proficient", "expertise", "accomplished"
    ]):
        score += 0.3

    # Check for job-specific relevance (0.25)
    if job_description:
        job_keywords = job_description.lower().split()
        matching_keywords = sum(1 for kw in job_keywords if len(kw) > 3 and kw in cover_letter_lower)
        relevance_score = min(matching_keywords / 5, 0.25)  # Max 0.25
        score += relevance_score
    else:
        score += 0.15  # Partial credit if no job description provided

    # Check for call-to-action (0.15)
    if any(cta in cover_letter_lower for cta in [
        "looking forward", "thank you", "sincerely", "regards", "interested"
    ]):
        score += 0.15

    # Check for length quality (0.1)
    if 50 < len(cover_letter.strip()) < 500:
        score += 0.1

    return min(score, 1.0)
