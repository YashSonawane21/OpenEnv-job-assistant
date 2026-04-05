from fastapi import FastAPI, HTTPException
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

app = FastAPI(title="OpenEnv Job Assistant", version="1.0.0")

# Add CORS middleware to allow cross-origin requests
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


# ----------- STATUS ENDPOINT -----------
@app.get("/status")
async def status():
    """Detailed status endpoint"""
    return {
        "name": "OpenEnv Job Assistant",
        "status": "running",
        "version": "1.0.0",
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