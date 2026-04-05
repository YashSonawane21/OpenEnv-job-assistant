"""
Task Manager
Enumerates and manages all job application tasks with their graders.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Callable, Dict, Any


class TaskType(Enum):
    """Supported task types."""
    RESUME = "resume"
    EMAIL = "email"
    COVER_LETTER = "cover_letter"
    LINKEDIN = "linkedin"
    INTERVIEW = "interview"


@dataclass
class Task:
    """Represents a job application task."""
    id: int
    name: str
    description: str
    type: TaskType
    grader: Callable
    max_score: float = 1.0

    def grade(self, submission: str, context: str = "") -> float:
        """
        Run the grader for this task.
        
        Args:
            submission: The user's submission
            context: Additional context (e.g., job description)
        
        Returns:
            float: Score between 0.0 and max_score
        """
        if context:
            score = self.grader(submission, context)
        else:
            score = self.grader(submission)
        
        # Ensure score is in valid range
        return max(0.0, min(float(score), self.max_score))


# Import all graders
from graders.resume_grader import grade_resume
from graders.email_grader import grade_email
from graders.cover_letter_grader import grade_cover_letter
from graders.linkedin_grader import grade_linkedin_profile
from graders.interview_grader import grade_interview_prep


# Define all tasks
TASKS: Dict[TaskType, Task] = {
    TaskType.RESUME: Task(
        id=1,
        name="Resume Optimization",
        description="Tailor your resume to match the job description",
        type=TaskType.RESUME,
        grader=grade_resume,
        max_score=1.0
    ),
    TaskType.EMAIL: Task(
        id=2,
        name="Email Composition",
        description="Write a professional outreach email to the recruiter",
        type=TaskType.EMAIL,
        grader=grade_email,
        max_score=1.0
    ),
    TaskType.COVER_LETTER: Task(
        id=3,
        name="Cover Letter Writing",
        description="Craft a compelling cover letter for the position",
        type=TaskType.COVER_LETTER,
        grader=grade_cover_letter,
        max_score=1.0
    ),
    TaskType.LINKEDIN: Task(
        id=4,
        name="LinkedIn Profile Optimization",
        description="Complete and optimize your LinkedIn profile",
        type=TaskType.LINKEDIN,
        grader=grade_linkedin_profile,
        max_score=1.0
    ),
    TaskType.INTERVIEW: Task(
        id=5,
        name="Interview Preparation",
        description="Prepare interview responses using STAR method",
        type=TaskType.INTERVIEW,
        grader=grade_interview_prep,
        max_score=1.0
    ),
}


def get_all_tasks() -> list[Task]:
    """Get all available tasks."""
    return sorted(TASKS.values(), key=lambda t: t.id)


def get_task(task_type: TaskType) -> Task:
    """Get a specific task by type."""
    return TASKS.get(task_type)


def get_task_by_id(task_id: int) -> Task:
    """Get a specific task by ID."""
    for task in TASKS.values():
        if task.id == task_id:
            return task
    return None


def enumerate_tasks() -> Dict[str, Any]:
    """
    Enumerate all available tasks for the dashboard.
    
    Returns:
        Dictionary with task enumeration
    """
    return {
        "total_tasks": len(TASKS),
        "tasks": [
            {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "type": task.type.value,
                "max_score": task.max_score
            }
            for task in get_all_tasks()
        ]
    }
