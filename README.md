---
title: OpenEnv Job Assistant
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# OpenEnv Job Assistant

A comprehensive FastAPI-based job application environment with AI-powered task grading, deployed on Hugging Face Spaces.

## Features

- **5 Comprehensive Tasks**: Resume optimization, email composition, cover letter writing, LinkedIn profiling, and interview preparation
- **Automated Graders**: Each task includes intelligent scoring algorithms that return grades in the 0.0-1.0 range
- **RESTful API**: Complete web service with endpoints for task enumeration, submission grading, and project information
- **Production Ready**: CORS-enabled, request logging, error handling, and health monitoring
- **Beautiful Web Interface**: Clean HTML interface for easy access to all project information

## API Endpoints

- `GET /` - Project overview with detailed information about AI capabilities
- `GET /tasks` - List all 5 available tasks with descriptions
- `POST /grade` - Grade a submission for a specific task
- `GET /health` - Health check endpoint
- `GET /project-info` - Complete project information and test results

## AI Agent Capabilities

### Resume Grader
Analyzes resume quality by matching skills against job requirements:
- Python skill match: +0.5 points
- React skill match: +0.5 points

### Email Grader
Evaluates professional email tone:
- Contains greeting: +0.3 points
- Shows interest: +0.4 points
- Includes thank you: +0.3 points

### Cover Letter Grader
Assesses cover letter effectiveness:
- Professional greeting: +0.2 points
- Experience/skills mentioned: +0.3 points
- Job relevance: +0.25 points
- Call-to-action: +0.15 points
- Length quality: +0.1 points

### LinkedIn Grader
Reviews LinkedIn profile completeness:
- Professional photo: +0.15 points
- Compelling headline: +0.2 points
- Detailed bio: +0.25 points
- Skills listed: +0.15 points
- Experience details: +0.15 points
- Contact information: +0.1 points
- Recommendations: +0.05 points

### Interview Grader
Evaluates interview preparation using STAR method:
- STAR method keywords: +0.25 points
- Technical knowledge: +0.2 points
- Problem-solving approach: +0.2 points
- Company research: +0.15 points
- Response depth: +0.1 points
- Practice/mock interview: +0.1 points

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn inference:app --host 0.0.0.0 --port 7860

# Or run the server version
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

## Testing

Run the comprehensive test suite:

```bash
python test_graders.py
```

All 15 tests should pass, validating that graders return scores in the correct 0.0-1.0 range.

## Deployment

The application is configured for deployment on Hugging Face Spaces with Docker:

- **Main App**: `inference.py` (primary deployment)
- **Server App**: `server/app.py` (alternative deployment)
- **Container**: Python 3.10 with FastAPI and Uvicorn
- **Port**: 7860 (HF Spaces standard)

## Project Structure

```
openenv-job-assistant/
├── inference.py              # Main FastAPI application
├── server/
│   ├── app.py               # Alternative server deployment
│   └── __init__.py          # Python package marker
├── graders/
│   ├── task_manager.py      # Task enumeration and management
│   ├── resume_grader.py     # Resume scoring logic
│   ├── email_grader.py      # Email scoring logic
│   ├── cover_letter_grader.py # Cover letter scoring logic
│   ├── linkedin_grader.py   # LinkedIn scoring logic
│   └── interview_grader.py  # Interview scoring logic
├── test_graders.py          # Comprehensive test suite
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── pyproject.toml           # Python project metadata
├── openenv.yaml            # Project configuration
└── README.md               # This documentation
```

## API Usage Examples

### Get All Tasks
```bash
curl https://yashs21-openenv-job-assistant.hf.space/tasks
```

### Grade a Resume
```bash
curl -X POST https://yashs21-openenv-job-assistant.hf.space/grade \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": 1,
    "submission": "Python developer with React expertise",
    "context": "Looking for Python + React engineer"
  }'
```

### Get Project Information
```bash
curl https://yashs21-openenv-job-assistant.hf.space/project-info
```

## Built With

- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for production deployment
- **Docker**: Containerization for consistent deployment

---

**Version**: 2.0.0
**Deployment**: Hugging Face Spaces
**License**: MIT
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