from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI()

# ----------- Global State -----------
state = {}

# ----------- Request Model -----------
class ActionRequest(BaseModel):
    action: str


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

    return {
        "observation": state,
        "info": {}
    }


# ----------- STEP ENDPOINT -----------
@app.post("/step")
def step(request: ActionRequest) -> Dict[str, Any]:
    global state

    action = request.action
    reward = 0
    done = False

    # ---- Action Handling ----
    if action == "modify_resume":
        state["resume"] = "Improved resume with relevant skills"
        reward += 1

    elif action == "write_email":
        state["email"] = "Professional email to recruiter"
        reward += 1

    elif action == "apply_job":
        if state["email"]:
            state["status"] = "applied"
            reward += 2
            done = True
        else:
            reward -= 1

    else:
        reward -= 1  # invalid action penalty

    return {
        "observation": state,
        "reward": reward,
        "done": done,
        "info": {}
    }


# ----------- ROOT CHECK (OPTIONAL) -----------
@app.get("/")
def home():
    return {"message": "OpenEnv Job Assistant is running"}


# ----------- HEALTH CHECK -----------
@app.get("/health")
async def health_check():
    """Endpoint for health checks"""
    return {"status": "healthy", "state_initialized": bool(state)}


# ----------- STARTUP/SHUTDOWN EVENTS -----------
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    try:
        logger.info("Startup complete!")
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")


# ----------- GLOBAL EXCEPTION HANDLER -----------
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )