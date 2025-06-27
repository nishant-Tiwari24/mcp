# langchain_mcp

This repository demonstrates a minimal working MCP (Multi-Server Control Plane) setup using LangChain, with:
- A dummy jobs and employee API (FastAPI)
- Two MCP servers (jobs and employee feedback, each on its own port)
- A Python client that can query both servers simultaneously (multi-server, multi-tool)

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

### 2. Start both MCP servers (in a new terminal)
```sh
python run_servers.py
```
This will start:
- Jobs server on port 8000
- Employee server on port 8002

Or, to run them manually in separate terminals:
```sh
python mcp_server/server.py jobs
python mcp_server/server.py employee
```

### 3. Run the multi-server client (in a new terminal)
```sh
python langchain_mcp_client.py
```
- The client will connect to both servers and can use tools from both in a single conversation.
- Make sure your OpenAI API key is exported or in a `.env` file.

---

## File Structure
- `langchain_mcp_client.py` — Python client for querying both MCP servers (multi-server, multi-tool)
- `mcp_server/server.py` — MCP servers (jobs and employee feedback, each on its own port)
- `mcp_server/jobs_api.py` — Dummy FastAPI backend for jobs and employee data
- `run_servers.py` — Script to start both MCP servers at once
- `requirements.txt` — Python dependencies
- `.gitignore` — Excludes `.venv`, `.env`, and other environment files

---

## Notes
- The `.venv` directory and `.env` file are not included in the repo. You must create them locally.
- Only the minimal, required files are tracked in git.
- If you want to add a frontend, you can do so separately (not included in this repo).

---

## Example Usage
- **Multi-server client:**
  - Query: "I need to find similar jobs for an AI engineer position in San Jose, CA with 4-5 years of experience, and also get a feedback summary for Kalyan P. Can you help me with both?"
  - The client will use both tools: `find_similar_jobs` and `summarize_employee_feedback`.

---

## License
MIT
