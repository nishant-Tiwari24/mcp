from mcp.server.fastmcp import FastMCP
import requests
import sys

# Server 1: jobs_server
jobs_server = FastMCP("jobs_server", port=8000)

@jobs_server.tool()
async def find_similar_jobs(requirements: str):
    """
    Given a prompt describing a job requisition (requirements, skills, location, etc.),
    return a list of similar jobs from the local jobs API.
    """
    # Call the dummy jobs API
    resp = requests.get("http://127.0.0.1:8001/jobs")
    jobs = resp.json().get("jobs", [])
    # Simple matching: check if requirements words appear in job fields
    req = requirements.lower()
    matches = []
    for job in jobs:
        text = f"{job['title']} {job['location']} {job['experience']} {' '.join(job['skills'])} {job['description']}".lower()
        if any(word in text for word in req.split()):
            matches.append(job)
    # If no matches, return all jobs
    return matches if matches else jobs

# Server 2: employee_server
employee_server = FastMCP("employee_server", port=8002)

@employee_server.tool()
async def summarize_employee_feedback(name: str):
    """
    Given an employee name, return a summary of their feedback for the current year.
    """
    resp = requests.get(f"http://127.0.0.1:8001/employees/{name}")
    emp = resp.json()
    if "error" in emp:
        return emp["error"]
    feedbacks = emp.get("feedback", [])
    # Filter for current year (2024)
    year = 2024
    summary = []
    for fb in feedbacks:
        if fb["year"] == year:
            summary.append(f"[{fb['type']}] {fb['text']}")
    if not summary:
        return f"No feedback found for {name} in {year}."
    return f"Feedback summary for {name} ({year}):\n" + "\n".join(summary)

def run_server(server_type: str):
    """Run a specific server using SSE transport"""
    if server_type == "jobs":
        server = jobs_server
    elif server_type == "employee":
        server = employee_server
    else:
        print(f"Unknown server type: {server_type}")
        return
    
    print(f"Starting {server_type}_server")
    server.run(transport="sse")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python server.py <server_type>")
        print("server_type: jobs or employee")
        sys.exit(1)
    
    server_type = sys.argv[1]
    run_server(server_type)
