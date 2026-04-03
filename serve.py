import sys
import os
import time

# Fix import path for Hugging Face
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from env.environment import JobEnv
from env.models import JobAction
from tasks import tasks


def run_environment():
    env = JobEnv()

    print("Starting Environment...\n", flush=True)

    obs = env.reset()
    total_reward = 0.0

    done = False

    while not done:

        jd = obs.job_description.lower()

        # 🔥 Smart Resume based on job
        resume = "Basic developer"

        if "python" in jd:
            resume += " Python"
        if "react" in jd:
            resume += " React"
        if "sql" in jd:
            resume += " SQL"
        if "node" in jd:
            resume += " Node.js"

        # Step 1: Modify Resume
        action = JobAction(
            action_type="modify_resume",
            content=resume
        )

        obs, reward, done, info = env.step(action)

        print("Action:", action, flush=True)
        print("Reward:", reward, flush=True)
        print("Info:", info, flush=True)
        print("-----", flush=True)

        total_reward += reward

        if done:
            break

        # Step 2: Write Email
        action = JobAction(
            action_type="write_email",
            content="Hello, I am interested in this job. Thank you."
        )

        obs, reward, done, info = env.step(action)

        print("Action:", action, flush=True)
        print("Reward:", reward, flush=True)
        print("Info:", info, flush=True)
        print("-----", flush=True)

        total_reward += reward

        if done:
            break

        # Step 3: Apply Job
        action = JobAction(
            action_type="apply_job",
            content="Apply"
        )

        obs, reward, done, info = env.step(action)

        print("Action:", action, flush=True)
        print("Reward:", reward, flush=True)
        print("Info:", info, flush=True)
        print("-----", flush=True)

        total_reward += reward

    print("\nFinal Environment Reward:", total_reward, flush=True)

    # 🔥 Evaluate Tasks
    print("\nTask Scores:", flush=True)

    state = env.state()

    for task in tasks:
        score = task["grader"](state)
        print(f"{task['name']} → {score}", flush=True)


if __name__ == "__main__":
    run_environment()

    # 🔁 Keep app alive for Hugging Face
    print("\nEnvironment running... keeping alive...\n", flush=True)

    while True:
        print("Heartbeat: App is alive", flush=True)
        time.sleep(30)
