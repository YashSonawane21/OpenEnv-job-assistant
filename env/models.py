from pydantic import BaseModel, Field
from typing import Optional


# 👁️ What the AI sees
class JobObservation(BaseModel):
    job_description: str
    resume: str
    recruiter_email: Optional[str] = None
    status: str


# 🎯 What the AI can do
class JobAction(BaseModel):
    action_type: str   # modify_resume / write_email / apply_job
    content: str


# 🏆 Reward format
class JobReward(BaseModel):
    score: float
    feedback: str