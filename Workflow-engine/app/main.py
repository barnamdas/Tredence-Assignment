from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
import uvicorn
from app.models import (
    GraphCreateRequest, GraphCreateResponse,
    GraphRunRequest, GraphRunResponse,
    GraphStateResponse
)
from app.engine.graph import WorkflowGraph
from app.engine.executor import GraphExecutor
from app.storage.memory_store import MemoryStore
from app.tools.code_review import register_code_review_tools
import uuid

app = FastAPI(title="Workflow Engine API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage
graph_store = MemoryStore()
run_store = MemoryStore()
tool_registry: Dict[str, callable] = {}

# Register tools
register_code_review_tools(tool_registry)


@app.post("/graph/create", response_model=GraphCreateResponse)
async def create_graph(request: GraphCreateRequest):
    """Create a new workflow graph"""
    try:
        graph = WorkflowGraph(
            nodes=request.nodes,
            edges=request.edges,
            tool_registry=tool_registry
        )
        
        graph_id = str(uuid.uuid4())
        graph_store.set(graph_id, graph)
        
        return GraphCreateResponse(graph_id=graph_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/graph/run", response_model=GraphRunResponse)
async def run_graph(request: GraphRunRequest):
    """Execute a workflow graph"""
    try:
        graph = graph_store.get(request.graph_id)
        if not graph:
            raise HTTPException(status_code=404, detail="Graph not found")
        
        executor = GraphExecutor(graph)
        run_id = str(uuid.uuid4())
        
        final_state, logs = await executor.execute(request.initial_state)
        
        run_store.set(run_id, {
            "graph_id": request.graph_id,
            "final_state": final_state,
            "logs": logs,
            "status": "completed"
        })
        
        return GraphRunResponse(
            run_id=run_id,
            final_state=final_state,
            logs=logs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/graph/state/{run_id}", response_model=GraphStateResponse)
async def get_graph_state(run_id: str):
    """Get the state of a workflow run"""
    run_data = run_store.get(run_id)
    if not run_data:
        raise HTTPException(status_code=404, detail="Run not found")
    
    return GraphStateResponse(
        run_id=run_id,
        graph_id=run_data["graph_id"],
        state=run_data["final_state"],
        logs=run_data["logs"],
        status=run_data["status"]
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)