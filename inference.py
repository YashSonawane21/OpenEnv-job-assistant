from fastapi import FastAPI

app = FastAPI()

state = {}

@app.post("/reset")
def reset():
    global state
    state = {
        "job_description": "Software Engineer",
        "resume": "Basic Resume",
        "email": "",
        "status": "not_applied"
    }
    return {
        "observation": state,
        "info": {}
    }

@app.post("/step")
def step(action: dict):
    global state

    act = action.get("action")
    reward = 0

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
        else:
            reward -= 1

    return {
        "observation": state,
        "reward": reward,
        "done": state["status"] == "applied",
        "info": {}
    }
