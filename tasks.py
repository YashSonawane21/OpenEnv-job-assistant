from graders.resume_grader import grade_resume
from graders.email_grader import grade_email


tasks = [
    {
        "name": "easy_resume",
        "description": "Improve resume to match job description",
        "grader": lambda state: grade_resume(
            state["resume"], state["job_description"]
        )
    },
    {
        "name": "medium_email",
        "description": "Write a professional recruiter email",
        "grader": lambda state: grade_email(
            state["recruiter_email"]
        )
    },
    {
        "name": "hard_full",
        "description": "Complete full job application process correctly",
        "grader": lambda state: (
            (1.0 if state["status"] == "applied" else 0.0) * 0.4 +
            grade_resume(state["resume"], state["job_description"]) * 0.3 +
            grade_email(state["recruiter_email"]) * 0.3
        )
    }
]