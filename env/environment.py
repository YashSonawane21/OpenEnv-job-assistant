import random
from env.models import JobObservation, JobAction


class JobEnv:

    def __init__(self):
        self._state = {}
        self._done = False

    def reset(self) -> JobObservation:
        jobs = [
            {
                "job_description": "Looking for Python + React developer",
                "resume": "Basic Python developer"
            },
            {
                "job_description": "Data Analyst with SQL and Excel",
                "resume": "Beginner data enthusiast"
            },
            {
                "job_description": "Backend Developer (Node.js, APIs)",
                "resume": "JavaScript beginner"
            }
        ]

        job = random.choice(jobs)

        self._state = {
            "job_description": job["job_description"],
            "resume": job["resume"],
            "recruiter_email": None,
            "status": "not_applied"
        }

        self._done = False
        return JobObservation(**self._state)

    def step(self, action: JobAction):
        reward = 0.0
        feedback = ""

        # 🟢 Resume Improvement (Smart Matching)
        if action.action_type == "modify_resume":
            jd = self._state["job_description"].lower()
            resume = action.content.lower()

            score_gain = 0

            if "python" in jd and "python" in resume:
                score_gain += 0.2
            if "react" in jd and "react" in resume:
                score_gain += 0.2
            if "sql" in jd and "sql" in resume:
                score_gain += 0.2
            if "node" in jd and "node" in resume:
                score_gain += 0.2

            reward += score_gain
            feedback = f"Matched skills score: {score_gain}"

            self._state["resume"] = action.content

        # 🟡 Email Writing
        elif action.action_type == "write_email":
            if action.content:
                reward += 0.3
                feedback = "Email written"
            else:
                reward -= 0.2
                feedback = "Empty email"

            self._state["recruiter_email"] = action.content

        # 🔴 Apply Job (with constraint)
        elif action.action_type == "apply_job":
            if not self._state["recruiter_email"]:
                reward -= 0.3
                feedback = "Cannot apply without email"
            else:
                reward += 0.3
                feedback = "Applied successfully"
                self._state["status"] = "applied"
                self._done = True

        # ❌ Invalid
        else:
            reward -= 0.5
            feedback = "Invalid action"

        return (
            JobObservation(**self._state),
            reward,
            self._done,
            {"feedback": feedback}
        )

    def state(self):
        return self._state