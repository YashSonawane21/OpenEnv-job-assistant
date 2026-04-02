from env.environment import JobEnv
from env.models import JobAction

env = JobEnv()

obs = env.reset()
print("Initial:", obs)

action = JobAction(
    action_type="modify_resume",
    content="Python + React Developer"
)

obs, reward, done, info = env.step(action)

print("After Step:", obs)
print("Reward:", reward)
print("Done:", done)
print("Info:", info)