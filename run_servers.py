#!/usr/bin/env python3
import subprocess
import time
import sys
import os

def run_servers():
    """Run both MCP servers simultaneously"""
    print("Starting both MCP servers...")
    
    # Start jobs server (port 8000 defined in constructor)
    jobs_process = subprocess.Popen([
        sys.executable, "mcp_server/server.py", "jobs"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("Jobs server started on port 8000")
    
    # Wait a moment for the first server to start
    time.sleep(2)
    
    # Start employee server (port 8001 defined in constructor)
    employee_process = subprocess.Popen([
        sys.executable, "mcp_server/server.py", "employee"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("Employee server started on port 8002")
    print("\nBoth servers are running!")
    print("Jobs server: http://127.0.0.1:8000")
    print("Employee server: http://127.0.0.1:8002")
    print("\nPress Ctrl+C to stop all servers")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        jobs_process.terminate()
        employee_process.terminate()
        print("Servers stopped")

if __name__ == "__main__":
    run_servers() 