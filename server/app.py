from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import logging
import sys
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    force=True
)
logger = logging.getLogger(__name__)

app = FastAPI(title="OpenEnv Job Assistant", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
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
        logger.error(f"❌ Error processing request: {e}", exc_info=True)
        raise

state = {}

# ----------- Request Models -----------
class ActionRequest(BaseModel):
    action: str


class GradeSubmissionRequest(BaseModel):
    task_id: int
    submission: str
    context: str = ""


# ----------- Import Task Manager -----------
try:
    from graders.task_manager import enumerate_tasks, get_task_by_id
    tasks_available = True
except ImportError:
    logger.warning("Task manager not available - tasks endpoints will be limited")
    tasks_available = False


# ----------- TASKS ENUMERATION ENDPOINT -----------
@app.get("/tasks")
async def get_tasks():
    """Get all available tasks with descriptions"""
    if not tasks_available:
        return {"error": "Tasks module not available"}
    
    try:
        tasks_info = enumerate_tasks()
        logger.info(f"📋 Enumerated {tasks_info['total_tasks']} tasks")
        return tasks_info
    except Exception as e:
        logger.error(f"Error enumerating tasks: {e}", exc_info=True)
        return {"error": str(e)}


# ----------- GRADE SUBMISSION ENDPOINT -----------
@app.post("/grade")
async def grade_submission(request: GradeSubmissionRequest) -> Dict[str, Any]:
    """Grade a submission for a specific task"""
    if not tasks_available:
        return {"error": "Grading not available"}
    
    try:
        task = get_task_by_id(request.task_id)
        if not task:
            logger.warning(f"⚠️ Task #{request.task_id} not found")
            return {"error": f"Task {request.task_id} not found"}
        
        score = task.grade(request.submission, request.context)
        logger.info(f"📊 Task #{request.task_id} ({task.name}): Score = {score:.2f}")
        
        return {
            "task_id": request.task_id,
            "task_name": task.name,
            "score": score,
            "max_score": task.max_score,
            "percentage": f"{(score/task.max_score)*100:.1f}%"
        }
    except Exception as e:
        logger.error(f"Error grading submission: {e}", exc_info=True)
        return {"error": str(e)}


# ----------- RESET ENDPOINT -----------
@app.post("/reset")
def reset() -> Dict[str, Any]:
    global state
    state = {
        "job_description": "Software Engineer (Python + React)",
        "resume": "Basic resume with limited skills",
        "email": "",
        "status": "not_applied"
    }
    logger.info("🔄 Environment reset")
    return {"observation": state, "info": {}}


# ----------- STEP ENDPOINT -----------
@app.post("/step")
def step(request: ActionRequest) -> Dict[str, Any]:
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
        "observation": state,
        "reward": reward,
        "done": done,
        "info": {}
    }


# ----------- ROOT CHECK -----------
@app.get("/")
def home():
    return {"message": "OpenEnv Job Assistant is running", "version": "2.0.0"}


# ----------- HEALTH CHECK -----------
@app.get("/health")
async def health_check():
    """Endpoint for health checks"""
    return {"status": "healthy", "state_initialized": bool(state)}


# ----------- STATUS ENDPOINT -----------
@app.get("/status")
async def status():
    """Detailed status endpoint"""
    return {
        "name": "OpenEnv Job Assistant",
        "status": "running",
        "version": "2.0.0",
        "timestamp": time.time(),
        "state": state
    }


# ----------- STARTUP/SHUTDOWN EVENTS -----------
@app.on_event("startup")
def startup_event():
    logger.info("🚀 Application starting up...")
    logger.info("✅ Startup complete!")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("🛑 Application shutting down...")


# ----------- GLOBAL EXCEPTION HANDLER -----------
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()