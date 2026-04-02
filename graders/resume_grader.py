def grade_resume(resume, job_description):
    score = 0.0

    # Check for required skills
    if "python" in resume.lower():
        score += 0.5

    if "react" in resume.lower():
        score += 0.5

    return min(score, 1.0)