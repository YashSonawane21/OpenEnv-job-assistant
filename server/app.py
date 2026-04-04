from fastapi import FastAPI
from typing import Dict, Any

app = FastAPI()

state = {}

@app.post("/reset")
def reset() -> Dict[str, Any]:
    global state
    state = {
        "job_description": "Software Engineer",
        "resume": "Basic resume",
        "email": "",
        "status": "not_applied"
    }
    return {"observation": state, "info": {}}

@app.post("/step")
def step(action: dict = {}) -> Dict[str, Any]:
    global state

    act = action.get("action", "")
    reward = 0
    done = False

    if act == "modify_resume":
        state["resume"] = "Improved Resume"
        reward += 1

    elif act == "write_email":
        state["email"] = "Professional Email"
        reward += 1

    elif act == "apply_job":
        if state["email"]:
            state["status"] = "applied"
            reward += 2
            done = True
        else:
            reward -= 1

    return {
        "observation": state,
        "reward": reward,
        "done": done,
        "info": {}
    }