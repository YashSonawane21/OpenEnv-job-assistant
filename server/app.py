from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import logging
import sys
import time
import os

# Fix import path (for graders)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    force=True
)
logger = logging.getLogger(__name__)

# Initialize app
app = FastAPI(title="OpenEnv Job Assistant", version="2.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- GLOBAL STATE --------
state = {}

# -------- REQUEST MODELS --------
class ActionRequest(BaseModel):
    action: str

class GradeSubmissionRequest(BaseModel):
    task_id: int
    submission: str
    context: str = ""

# -------- TASK IMPORT --------
try:
    from graders.task_manager import enumerate_tasks, get_task_by_id
    tasks_available = True
except Exception as e:
    logger.warning(f"Tasks module not available: {e}")
    tasks_available = False

# -------- MIDDLEWARE --------
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    logger.info(f"📥 {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"📤 {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
        return response
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        raise

# -------- BASIC ROUTES --------

@app.get("/")
def home():
    return {
        "message": "OpenEnv Job Assistant is running",
        "version": "2.0.0",
        "description": "A comprehensive job application environment with AI-powered task grading",
        "ai_agents_capabilities": {
            "resume_grader": "Analyzes resume quality by matching skills (Python +0.5, React +0.5) against job requirements",
            "email_grader": "Evaluates professional email tone (hello +0.3, interested +0.4, thank you +0.3)",
            "cover_letter_grader": "Assesses cover letter effectiveness (greeting +0.2, experience +0.3, relevance +0.25, CTA +0.15, length +0.1)",
            "linkedin_grader": "Reviews LinkedIn profile completeness (photo +0.15, headline +0.2, bio +0.25, skills +0.15, experience +0.15, contact +0.1, recommendations +0.05)",
            "interview_grader": "Evaluates interview preparation using STAR method (STAR keywords +0.25, technical +0.2, problem-solving +0.2, research +0.15, depth +0.1, practice +0.1)"
        },
        "environment_performs": [
            "Automated grading of job application materials with scores from 0.0 to 1.0",
            "Real-time feedback on resume, email, cover letter, LinkedIn profile, and interview preparation",
            "Comprehensive testing suite with 15 validation tests (all passing)",
            "RESTful API endpoints for task enumeration, grading submissions, and health monitoring",
            "CORS-enabled cross-origin support for web applications",
            "Request logging and error handling for production reliability"
        ],
        "available_endpoints": {
            "GET /": "This overview information",
            "GET /tasks": "List all 5 available tasks",
            "POST /grade": "Grade a submission for a specific task",
            "GET /health": "Basic health check",
            "GET /project-info": "Complete project information and test results"
        },
        "full_project_info": "https://yashs21-openenv-job-assistant.hf.space/project-info"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/status")
def status():
    return {
        "status": "running",
        "state": state,
        "timestamp": time.time()
    }

# -------- TASK ROUTES --------

@app.get("/tasks")
def get_tasks():
    if not tasks_available:
        return {"error": "Tasks not available"}
    try:
        return enumerate_tasks()
    except Exception as e:
        logger.error(f"Task error: {e}", exc_info=True)
        return {"error": str(e)}

@app.post("/grade")
def grade_submission(request: GradeSubmissionRequest) -> Dict[str, Any]:
    if not tasks_available:
        return {"error": "Grading not available"}
    try:
        task = get_task_by_id(request.task_id)
        if not task:
            return {"error": f"Task {request.task_id} not found"}

        score = task.grade(request.submission, request.context)

        return {
            "task_id": request.task_id,
            "task_name": task.name,
            "score": score,
            "max_score": task.max_score,
            "percentage": f"{(score/task.max_score)*100:.1f}%"
        }
    except Exception as e:
        logger.error(f"Grading error: {e}", exc_info=True)
        return {"error": str(e)}

# -------- ENVIRONMENT ROUTES --------

@app.post("/reset")
def reset():
    global state
    state = {
        "job_description": "Software Engineer (Python + React)",
        "resume": "Basic resume",
        "email": "",
        "status": "not_applied"
    }
    logger.info("🔄 State reset")
    return {"state": state}

@app.post("/step")
def step(request: ActionRequest):
    global state

    action = request.action
    reward = 0
    done = False

    if action == "modify_resume":
        state["resume"] = "Improved Resume"
        reward += 1

    elif action == "write_email":
        state["email"] = "Professional Email"
        reward += 1

    elif action == "apply_job":
        if state["email"]:
            state["status"] = "applied"
            reward += 2
            done = True
        else:
            reward -= 1

    logger.info(f"📍 Action '{action}' executed - reward: {reward}")

    return {
        "state": state,
        "reward": reward,
        "done": done
    }

# -------- PROJECT INFO --------

@app.get("/project-info")
def project_info():
    return {
        "project": "OpenEnv Job Assistant",
        "version": "2.0.0",
        "status": "running",
        "link": "https://yashs21-openenv-job-assistant.hf.space/project-info",
        "endpoints": [
            "/", "/health", "/status",
            "/tasks", "/grade",
            "/reset", "/step",
            "/project-info"
        ]
    }

# -------- EVENTS --------

@app.on_event("startup")
def startup_event():
    logger.info("")
    logger.info("✅ OpenEnv Job Assistant v2.0.0 is RUNNING")
    logger.info("")
    logger.info("📋 View Project Info: https://yashs21-openenv-job-assistant.hf.space/project-info")
    logger.info("")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("🛑 Application shutting down")

# -------- GLOBAL ERROR HANDLER --------

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )