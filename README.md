---
title: OpenEnv Job Assistant
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# OpenEnv Job Assistant Environment

## Description
This project simulates a real-world job application workflow where an AI agent learns how to:
- Improve resumes
- Write recruiter emails
- Apply for jobs

---

## Real-World Scenarios

This environment simulates multiple job roles:

- Software Engineer (Python + React)
- Data Analyst (SQL + Excel)
- Backend Developer (Node.js APIs)

The agent must adapt its actions depending on job requirements.

---

## Environment Design

### Observation Space
- job_description
- resume
- recruiter_email
- application status

### Action Space
- modify_resume
- write_email
- apply_job

---

## Tasks & Graders

The environment provides **5 comprehensive tasks** with automated graders that provide scores in the **0.0–1.0 range**:

### 1. Resume Optimization
**Goal:** Tailor your resume to match the job description  
**Grader:** `grade_resume(resume, job_description)`  
**Scoring:**
- Python skill match: +0.5
- React skill match: +0.5

**Example:**
```bash
curl -X POST https://yashsonawane-log-analyzer.hf.space/grade \
  -H 'Content-Type: application/json' \
  -d '{
    "task_id": 1,
    "submission": "Python developer with React expertise",
    "context": "Looking for Python + React engineer"
  }'
```

### 2. Email Composition
**Goal:** Write a professional outreach email to the recruiter  
**Grader:** `grade_email(email)`  
**Scoring:**
- Contains "hello": +0.3
- Contains "interested": +0.4
- Contains "thank you": +0.3

### 3. Cover Letter Writing (NEW)
**Goal:** Craft a compelling cover letter for the position  
**Grader:** `grade_cover_letter(cover_letter, job_description)`  
**Scoring:**
- Professional greeting: +0.2
- Personal experience/skills: +0.3
- Job-specific relevance: +0.25
- Call-to-action: +0.15
- Length quality (50-500 chars): +0.1

### 4. LinkedIn Profile Optimization (NEW)
**Goal:** Complete and optimize your LinkedIn profile  
**Grader:** `grade_linkedin_profile(profile_data)`  
**Scoring:**
- Professional photo mention: +0.15
- Professional headline: +0.2
- Detailed bio: +0.25 (progressive: 100+ chars = +0.15, 200+ chars = +0.1)
- Skills mentioned: +0.15
- Experience details: +0.15
- Contact/CTA: +0.1
- Recommendations: +0.05

### 5. Interview Preparation (NEW)
**Goal:** Prepare interview responses using STAR method  
**Grader:** `grade_interview_prep(preparation_notes, job_description)`  
**Scoring:**
- STAR method keywords: +0.25
- Technical knowledge: +0.2
- Problem-solving approach: +0.2
- Company/role research: +0.15
- Depth: +0.1 (progressive)
- Practice/mock interview mention: +0.1

---

## Reward System

- Skill matching → positive reward
- Writing email → reward
- Applying correctly → reward
- Applying without email → penalty
- Invalid actions → penalty

Reward is continuous and reflects partial progress.

---

## API Endpoints

### Enumerate Tasks
**GET** `/tasks`

Lists all 5 available tasks with descriptions and max scores.

**Response:**
```json
{
  "total_tasks": 5,
  "tasks": [
    {
      "id": 1,
      "name": "Resume Optimization",
      "type": "resume",
      "description": "Tailor your resume to match the job description",
      "max_score": 1.0
    },
    ...
  ]
}
```

### Grade Submission
**POST** `/grade`

Grade any submission for a specific task. Returns a score in the **0.0–1.0 range**.

**Request:**
```json
{
  "task_id": 1,
  "submission": "Python developer with React skills and 5 years experience",
  "context": "Looking for Python + React engineer with SQL expertise"
}
```

**Response:**
```json
{
  "task_id": 1,
  "task_name": "Resume Optimization",
  "score": 1.0,
  "max_score": 1.0,
  "percentage": "100.0%"
}
```

### Health Check
**GET** `/health`

Quick health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "state_initialized": true
}
```

### Status
**GET** `/status`

Detailed status with app info and current state.

**Response:**
```json
{
  "name": "OpenEnv Job Assistant",
  "status": "running",
  "version": "1.0.0",
  "timestamp": 1712282480.123,
  "state": {}
}
```

### Reset Environment
**POST** `/reset`

Initialize/reset the environment state.

### Step Action
**POST** `/step`

Perform an action in the environment.

---

## Project Structure

```
openenv-job-assistant/
├── graders/
│   ├── __init__.py
│   ├── resume_grader.py              # Grade resume (0.0-1.0)
│   ├── email_grader.py               # Grade email (0.0-1.0)
│   ├── cover_letter_grader.py        # Grade cover letter (0.0-1.0) - NEW
│   ├── linkedin_grader.py            # Grade LinkedIn profile (0.0-1.0) - NEW
│   ├── interview_grader.py           # Grade interview prep (0.0-1.0) - NEW
│   └── task_manager.py               # Task enumeration & management
├── env/
│   ├── __init__.py
│   ├── environment.py                # Job environment simulation
│   └── models.py                     # Pydantic models
├── inference.py                      # FastAPI server with endpoints
├── server.py                         # Alternative server setup
├── test_graders.py                   # Comprehensive test suite (✅ ALL PASSED)
├── Dockerfile                        # Container configuration
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── pyproject.toml                    # Project config
```

---

## Testing

Run the comprehensive test suite to validate all graders:

```bash
python test_graders.py
```

**Test Results:**
```
✅ Task #1: Resume Optimization - ALL PASSED
   ✓ PASS | Empty submission: 0.00
   ✓ PASS | Basic submission: 0.00
   ✓ PASS | Good match: 1.00

✅ Task #2: Email Composition - ALL PASSED
   ✓ PASS | Empty submission: 0.00
   ✓ PASS | Low quality: 0.00
   ✓ PASS | Professional: 1.00

✅ Task #3: Cover Letter Writing - ALL PASSED
   ✓ PASS | Empty submission: 0.00
   ✓ PASS | Short submission: 0.00
   ✓ PASS | Quality submission: 1.00

✅ Task #4: LinkedIn Profile Optimization - ALL PASSED
   ✓ PASS | Empty submission: 0.00
   ✓ PASS | Minimal profile: 0.20
   ✓ PASS | Complete profile: 0.90

✅ Task #5: Interview Preparation - ALL PASSED
   ✓ PASS | Empty submission: 0.00
   ✓ PASS | Vague response: 0.10
   ✓ PASS | STAR method: 0.73

ALL GRADERS VALIDATED: All scores return in 0.0-1.0 range ✅
```

---

## Local Development

### Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run Server
```bash
uvicorn inference:app --host 0.0.0.0 --port 7860 --reload
```

Access at: `http://localhost:7860`

### Test Graders
```bash
python test_graders.py
```

---

## Deployment

This project is containerized and deployed on [Hugging Face Spaces](https://huggingface.co/spaces).

**Container Features:**
- Logging middleware for all requests
- CORS enabled for cross-origin requests
- Health check endpoints
- Comprehensive error handling
- Automatic request/response logging

---

## Format & Score Validation

✅ **All tasks enforce score range:** 0.0 - 1.0  
✅ **Graders are idempotent:** Same input always produces same score  
✅ **Context-aware grading:** Uses job_description when provided  
✅ **Partial credit:** Progressive scoring based on submission quality  

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test with `python test_graders.py`
4. Submit a pull request

---

## License

MIT