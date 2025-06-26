# langchain_mcp

This repository demonstrates a minimal working MCP (Multi-Server Control Plane) setup using LangChain, with:
- A dummy jobs and employee API (FastAPI)
- Two MCP servers (jobs and employee feedback)
- A Python client that can query either server

---

## Requirements
- Python 3.9+
- [pip](https://pip.pypa.io/en/stable/)
- [Node.js](https://nodejs.org/) (optional, only if you want to build a frontend)
- An OpenAI API key (for GPT-4o)

---

## Setup

### 1. Clone the repository
```sh
git clone https://github.com/nishant-Tiwari24/mcp.git
cd mcp
```

### 2. Create and activate a virtual environment
```sh
python3 -m venv .venv
source .venv/bin/activate
```
> **Note:** `.venv` is gitignored. You must create it yourself.

### 3. Install Python dependencies
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set your OpenAI API key
Create a `.env` file in the project root (not tracked by git):
```
OPENAI_API_KEY=sk-...your-key-here...
```
Or export it in your shell before running the client:
```sh
export OPENAI_API_KEY=sk-...your-key-here...
```

---

## Running the Demo

### 1. Start the dummy jobs/employee API
```sh
uvicorn mcp_server.jobs_api:app --port 8001 --host 127.0.0.1
```

### 2. Start the MCP server (in a new terminal)
- For jobs server:
  ```sh
  python mcp_server/server.py
  ```
- For employee server:
  ```sh
  python mcp_server/server.py employee
  ```
> **Note:** Only one MCP server can run at a time (always on port 8000).

### 3. Run the client (in a new terminal)
- Edit `langchain_mcp_client.py` and set `SERVER = "jobs_server"` or `SERVER = "employee_server"` at the top.
- **Before running the client, make sure your OpenAI API key is exported:**
  ```sh
  export OPENAI_API_KEY=sk-...your-key-here...
  python langchain_mcp_client.py
  ```
  Or, if you have a `.env` file, just run:
  ```sh
  python langchain_mcp_client.py
  ```

---

## File Structure
- `langchain_mcp_client.py` — Python client for querying MCP servers
- `mcp_server/server.py` — MCP server (jobs or employee feedback)
- `mcp_server/jobs_api.py` — Dummy FastAPI backend for jobs and employee data
- `requirements.txt` — Python dependencies
- `.gitignore` — Excludes `.venv`, `.env`, and other environment files

---

## Notes
- The `.venv` directory and `.env` file are not included in the repo. You must create them locally.
- Only the minimal, required files are tracked in git.
- If you want to add a frontend, you can do so separately (not included in this repo).

---

## Example Usage
- **Jobs server:**
  - Query: "I am looking for an AI engineer in San Jose, CA with 4-5 years of experience leveraging models like GPT 401, Claude 3.5 or similar. Can you please show the similar jobs I can use to create a requisition?"
- **Employee server:**
  - Query: "I am requesting a feedback summary for Kalyan P. The system will pull calendar year feedback, including Props, and create a summary for me to review, which can be ideally entered into Workday as an impact summary."

---

## License
MIT
