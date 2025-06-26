from mcp.server.fastmcp import FastMCP
import requests

# Server 1: jobs_server
jobs_server = FastMCP("jobs_server")

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
employee_server = FastMCP("employee_server")

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

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "employee":
        employee_server.run(transport="sse")
    else:
        jobs_server.run(transport="sse")
