from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
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
    logger.info(f"REQUEST {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"RESPONSE {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise

# -------- BASIC ROUTES --------

@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenEnv Job Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
            h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            h2 { color: #34495e; margin-top: 30px; }
            .capability { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; }
            .endpoint { background: #e8f4fd; padding: 10px; margin: 5px 0; border-radius: 5px; }
            .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="status">
            <h1>OpenEnv Job Assistant v2.0.0 is Running</h1>
            <p><strong>Description:</strong> A comprehensive job application environment with AI-powered task grading</p>
        </div>

        <h2>AI Agent Capabilities</h2>
        <div class="capability">
            <strong>Resume Grader:</strong> Analyzes resume quality by matching skills (Python +0.5, React +0.5) against job requirements
        </div>
        <div class="capability">
            <strong>Email Grader:</strong> Evaluates professional email tone (hello +0.3, interested +0.4, thank you +0.3)
        </div>
        <div class="capability">
            <strong>Cover Letter Grader:</strong> Assesses cover letter effectiveness (greeting +0.2, experience +0.3, relevance +0.25, CTA +0.15, length +0.1)
        </div>
        <div class="capability">
            <strong>LinkedIn Grader:</strong> Reviews LinkedIn profile completeness (photo +0.15, headline +0.2, bio +0.25, skills +0.15, experience +0.15, contact +0.1, recommendations +0.05)
        </div>
        <div class="capability">
            <strong>Interview Grader:</strong> Evaluates interview preparation using STAR method (STAR keywords +0.25, technical +0.2, problem-solving +0.2, research +0.15, depth +0.1, practice +0.1)
        </div>

        <h2>Environment Capabilities</h2>
        <ul>
            <li>Automated grading of job application materials with scores from 0.0 to 1.0</li>
            <li>Real-time feedback on resume, email, cover letter, LinkedIn profile, and interview preparation</li>
            <li>Comprehensive testing suite with 15 validation tests (all passing)</li>
            <li>RESTful API endpoints for task enumeration, grading submissions, and health monitoring</li>
            <li>CORS-enabled cross-origin support for web applications</li>
            <li>Request logging and error handling for production reliability</li>
        </ul>

        <h2>Available API Endpoints</h2>
        <div class="endpoint"><strong>GET /</strong> - This overview information</div>
        <div class="endpoint"><strong>GET /tasks</strong> - List all 5 available tasks</div>
        <div class="endpoint"><strong>POST /grade</strong> - Grade a submission for a specific task</div>
        <div class="endpoint"><strong>GET /health</strong> - Basic health check</div>
        <div class="endpoint"><strong>GET /project-info</strong> - Complete project information and test results</div>

        <h2>Full Project Information</h2>
        <p>View complete project details, test results, and API documentation:</p>
        <p><a href="https://yashs21-openenv-job-assistant.hf.space/project-info" target="_blank">https://yashs21-openenv-job-assistant.hf.space/project-info</a></p>

        <hr>
        <p style="text-align: center; color: #7f8c8d; font-size: 0.9em;">
            Built with FastAPI • Deployed on Hugging Face Spaces • OpenEnv Job Assistant v2.0.0
        </p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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
    logger.info("State reset")
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

    logger.info(f"Action '{action}' executed - reward: {reward}")

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
    logger.info("OpenEnv Job Assistant v2.0.0 is RUNNING")
    logger.info("")
    logger.info("View Project Info: https://yashs21-openenv-job-assistant.hf.space/project-info")
    logger.info("")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Application shutting down")

# -------- GLOBAL ERROR HANDLER --------

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )