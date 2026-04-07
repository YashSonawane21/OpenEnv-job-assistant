---
title: OpenEnv Job Assistant
emoji: "🤖"
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# OpenEnv Job Assistant

A FastAPI-based job application environment with deterministic, explainable graders across five tasks:

1. Resume Optimization
2. Email Composition
3. Cover Letter Writing
4. LinkedIn Profile Optimization
5. Interview Preparation

## What Makes This Version Stronger

- Rubric-based scoring instead of simple keyword-only scoring
- Structured grading output with criterion-level breakdown
- Actionable feedback: strengths, improvements, and penalties
- Anti-gaming checks (keyword stuffing/repetition penalties)
- New holistic endpoint: `POST /grade-all` for overall readiness report
- Deterministic outputs suitable for validator and judge consistency

## API Endpoints

- `GET /` - Project home
- `GET /tasks` - Enumerate all available tasks
- `POST /grade` - Grade a single task with detailed feedback
- `POST /grade-all` - Grade all five artifacts and return readiness report
- `GET /health` - Health check
- `GET /status` - Runtime status and state
- `POST /reset` - Reset environment state
- `POST /step` - Environment action step
- `GET /project-info` - Full project metadata and capability summary

## `/grade` Example

### Request

```bash
curl -X POST https://yashs21-openenv-job-assistant.hf.space/grade \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": 1,
    "submission": "Python developer with React and SQL experience delivering backend APIs",
    "context": "Looking for Python + React engineer with data experience"
  }'
```

### Response (shape)

```json
{
  "task_id": 1,
  "task_name": "Resume Optimization",
  "task_type": "resume",
  "score": 0.84,
  "raw_score": 0.84,
  "max_score": 1.0,
  "percentage": "84.0%",
  "rubric_breakdown": [
    {
      "criterion": "Skill coverage: python",
      "score": 0.18,
      "max_score": 0.18,
      "met": true
    }
  ],
  "strengths": [
    "Resume shows broad skill coverage across engineering competencies."
  ],
  "improvements": [
    "Mirror more role-specific keywords from the job description."
  ],
  "penalties": [],
  "quality_flags": {
    "empty_submission": false,
    "keyword_stuffing": false
  }
}
```

## `/grade-all` Example

### Request

```bash
curl -X POST https://yashs21-openenv-job-assistant.hf.space/grade-all \
  -H "Content-Type: application/json" \
  -d '{
    "resume": "Python + React engineer with SQL and delivery impact",
    "email": "Hello, I am interested in this role and can share relevant projects. Thank you.",
    "cover_letter": "Dear Hiring Manager, I have delivered Python and React systems...",
    "linkedin_profile": "Professional photo. Senior developer. Skills: Python, React, SQL...",
    "interview_notes": "Situation... Task... Action... Result...",
    "job_description": "Hiring software engineer with Python, React, SQL, and communication skills."
  }'
```

### Response (shape)

```json
{
  "overall_readiness_score": 0.79,
  "overall_readiness_percentage": "79.0%",
  "task_results": [],
  "priority_actions": [
    "Cover Letter Writing: Reflect more terms from the job description to show fit."
  ],
  "judging_signals": [
    "Deterministic rubric grading",
    "Anti-keyword-stuffing penalties",
    "Criterion-level explainability"
  ]
}
```

## Local Development

```bash
pip install -r requirements.txt
uvicorn inference:app --host 0.0.0.0 --port 7860 --reload
```

Alternative entrypoint:

```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload
```

## Testing

Run:

```bash
python test_graders.py
```

This validates:

- Score range safety (0.0 to 1.0 bounds)
- Deterministic grading (same input, same output)
- Basic robustness including keyword stuffing cases

## Deployment

- Platform: Hugging Face Spaces
- Runtime: Docker + Python 3.10
- Framework: FastAPI + Uvicorn
- Main app: `inference.py`
- Compatibility app: `server/app.py`

## Project Structure

```text
openenv-job-assistant/
├── inference.py
├── server/
│   ├── app.py
│   └── __init__.py
├── graders/
│   ├── task_manager.py
│   ├── resume_grader.py
│   ├── email_grader.py
│   ├── cover_letter_grader.py
│   ├── linkedin_grader.py
│   └── interview_grader.py
├── test_graders.py
├── requirements.txt
├── Dockerfile
├── pyproject.toml
└── README.md
```

## License

MIT
