# Workflow Engine

A lightweight workflow/graph execution engine built with FastAPI.

## Features

- **Node-based workflow execution**: Define nodes as Python functions
- **State management**: Shared state flows through the workflow
- **Conditional branching**: Route execution based on state values
- **Loop support**: Execute nodes repeatedly until conditions are met
- **Tool registry**: Register and reuse tools across workflows
- **REST API**: Create and execute workflows via HTTP endpoints

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python -m app.main
```

Or:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## API Endpoints

### POST /graph/create
Create a new workflow graph.

**Request body:**
```json
{
  "nodes": [
    {"name": "extract", "tool": "extract_functions"},
    {"name": "check", "tool": "check_complexity"},
    {"name": "detect", "tool": "detect_issues"},
    {"name": "suggest", "tool": "suggest_improvements"}
  ],
  "edges": [
    {"from_node": "extract", "to_node": "check"},
    {"from_node": "check", "to_node": "detect"},
    {"from_node": "detect", "to_node": "suggest"}
  ]
}
```

### POST /graph/run
Execute a workflow graph.

**Request body:**
```json
{
  "graph_id": "uuid-here",
  "initial_state": {
    "code": "def hello():\n    print('world')"
  }
}
```

### GET /graph/state/{run_id}
Get the state and logs of a completed run.

## Example Workflow: Code Review Agent

The included example implements a code review workflow:

1. **Extract functions**: Parse function definitions from code
2. **Check complexity**: Analyze code complexity metrics
3. **Detect issues**: Find common code quality issues
4. **Suggest improvements**: Generate improvement suggestions

## Architecture

- `app/main.py`: FastAPI application and endpoints
- `app/models.py`: Pydantic models for requests/responses
- `app/engine/graph.py`: Workflow graph structure and validation
- `app/engine/executor.py`: Graph execution engine
- `app/tools/`: Tool implementations
- `app/storage/`: Storage backends

## What Could Be Improved

With more time, I would add:

1. **Persistent storage**: SQLite/PostgreSQL instead of in-memory
2. **WebSocket support**: Stream execution logs in real-time
3. **Parallel execution**: Run independent nodes concurrently
4. **Error handling**: Retry logic and graceful failure recovery
5. **Graph visualization**: Generate visual representations of workflows
6. **Advanced conditions**: Support for complex boolean logic
7. **Middleware**: Authentication, rate limiting, monitoring
8. **Testing**: Comprehensive unit and integration tests

## Example Usage

```python
import requests

# Create graph
response = requests.post("http://localhost:8000/graph/create", json={
    "nodes": [
        {"name": "extract", "tool": "extract_functions"},
        {"name": "analyze", "tool": "check_complexity"}
    ],
    "edges": [
        {"from_node": "extract", "to_node": "analyze"}
    ]
})
graph_id = response.json()["graph_id"]

# Run graph
response = requests.post("http://localhost:8000/graph/run", json={
    "graph_id": graph_id,
    "initial_state": {
        "code": "def example():\n    return 42"
    }
})
print(response.json())
```