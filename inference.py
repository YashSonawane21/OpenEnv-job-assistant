from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

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