from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy jobs data
dummy_jobs = [
    {
        "id": 1,
        "title": "AI Engineer",
        "location": "San Jose, CA",
        "experience": "4-5 years",
        "skills": ["GPT-4o", "Claude 3.5", "Python", "ML Ops"],
        "description": "Work on advanced AI models and deploy solutions.",
    },
    {
        "id": 2,
        "title": "Data Scientist",
        "location": "San Jose, CA",
        "experience": "3-5 years",
        "skills": ["Python", "TensorFlow", "Data Analysis"],
        "description": "Analyze data and build predictive models.",
    },
    {
        "id": 3,
        "title": "AI Engineer",
        "location": "Remote",
        "experience": "5+ years",
        "skills": ["Llama 3", "NLP", "Deep Learning"],
        "description": "Lead NLP projects and mentor junior engineers.",
    },
]

# Dummy employee feedback data
dummy_employees = [
    {
        "id": 1,
        "name": "Kalyan P.",
        "feedback": [
            {"year": 2024, "type": "Props", "text": "Great team player, delivered key project milestones."},
            {"year": 2024, "type": "Manager", "text": "Consistently exceeds expectations in AI research."},
            {"year": 2023, "type": "Peer", "text": "Very helpful and knowledgeable in ML topics."},
        ],
    },
    {
        "id": 2,
        "name": "Alex J.",
        "feedback": [
            {"year": 2024, "type": "Props", "text": "Excellent communication and leadership."},
        ],
    },
]

@app.get("/jobs")
def get_jobs():
    return {"jobs": dummy_jobs}

@app.get("/employees")
def get_employees():
    return {"employees": dummy_employees}

@app.get("/employees/{name}")
def get_employee_by_name(name: str):
    for emp in dummy_employees:
        if emp["name"].lower() == name.lower():
            return emp
    return {"error": "Employee not found"} 