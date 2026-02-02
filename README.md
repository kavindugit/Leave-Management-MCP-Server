# 🌴 Leave Management MCP Server

## Environment Setup

### Prerequisites

- Python 3.12+
- uv (fast Python package installer)

Install uv if it is not installed:

```
pip install uv
```

### Create and Activate Virtual Environment

```
uv venv
```

Windows:

```
.\.venv\Scripts\activate
```

---

## Install Dependencies

```
uv pip install "mcp[cli]" fastmcp
```

---

## Run

### Run Locally (Debug Mode)

```
uv run main.py
```

### Install and Run with Claude Desktop

```
uv run mcp install main.py --name LeaveManagement
```

After installation, fully quit Claude Desktop from the system tray and relaunch it.

Verify under:

```
Settings → Developer
```

You should see **LeaveManagement** running.
