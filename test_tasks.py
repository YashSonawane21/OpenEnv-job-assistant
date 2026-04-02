from env.environment import JobEnv
from tasks import tasks

env = JobEnv()
obs = env.reset()

# Simulate good actions
env._state["resume"] = "Python React Developer"
env._state["recruiter_email"] = "Hello, I am interested in this job. Thank you."

state = env.state()

for task in tasks:
    score = task["grader"](state)
    print(task["name"], "Score:", score)