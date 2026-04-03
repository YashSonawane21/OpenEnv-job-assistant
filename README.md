---
title: OpenEnv Job Assistant
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: baseline.py
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

## Tasks

### Easy Task
Improve resume based on job description

### Medium Task
Write a professional recruiter email

### Hard Task
Complete full job application process correctly:
- Resume matches job
- Email is written
- Application submitted

---

## Reward System

- Skill matching → positive reward
- Writing email → reward
- Applying correctly → reward
- Applying without email → penalty
- Invalid actions → penalty

Reward is continuous and reflects partial progress.

---

## Setup Instructions

```bash
pip install -r requirements.txt
python baseline.py

---

## Key Features

- 🔹 Multi-scenario job simulation  
- 🔹 Dynamic reward shaping  
- 🔹 Constraint-based action validation  
- 🔹 Progressive task difficulty (easy → hard)