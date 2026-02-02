import json
import os
import sys
from mcp.server.fastmcp import FastMCP

# Core Fix: Force the script to find its true absolute path
current_script_path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(current_script_path)
DATA_FILE = os.path.join(BASE_DIR, "leaves.json")


def load_data():
    """Load employee data from the JSON file."""
    # Debug: This will show up in the Claude MCP logs
    print(f"Server starting. Looking for data at: {DATA_FILE}", file=sys.stderr)

    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    """Write current data back to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Create MCP server
mcp = FastMCP("LeaveManagement")


# Tool: Check leave balance
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check how many leave days an employee has left."""
    employee_leaves = load_data()
    data = employee_leaves.get(employee_id)
    if data:
        return f"{employee_id} has {data['balance']} leave days remaining."
    return f"Employee ID {employee_id} not found."


# Tool: Apply for leave
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: list[str]) -> str:
    """Apply leave for specific dates (e.g., ["2025-03-12", "2025-04-15"])"""
    employee_leaves = load_data()

    if employee_id not in employee_leaves:
        return "Employee ID not found."

    request_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]["balance"]

    if available_balance < request_days:
        return f"Insufficient leave balance. You have {available_balance} days left."

    # Deduct balance and add to history
    employee_leaves[employee_id]["balance"] -= request_days
    employee_leaves[employee_id]["history"].extend(leave_dates)

    # Persist the change immediately
    save_data(employee_leaves)

    return f"Leave approved for {request_days} days. New balance is {employee_leaves[employee_id]['balance']} days."


# Tool: Get leave history
@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Get the leave history of an employee."""
    employee_leaves = load_data()
    data = employee_leaves.get(employee_id)
    if data:
        history = ', '.join(data['history']) if data['history'] else "No leaves taken."
        return f"Leave history for {employee_id}: {history}"
    return f"Employee ID {employee_id} not found."


# Resource: Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to the Leave Management System."


if __name__ == "__main__":
    mcp.run()