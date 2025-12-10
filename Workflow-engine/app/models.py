from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class NodeDefinition(BaseModel):
    name: str
    tool: str
    condition: Optional[Dict[str, Any]] = None


class EdgeDefinition(BaseModel):
    from_node: str
    to_node: str
    condition: Optional[Dict[str, Any]] = None


class GraphCreateRequest(BaseModel):
    nodes: List[NodeDefinition]
    edges: List[EdgeDefinition]


class GraphCreateResponse(BaseModel):
    graph_id: str


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]


class GraphRunResponse(BaseModel):
    run_id: str
    final_state: Dict[str, Any]
    logs: List[str]


class GraphStateResponse(BaseModel):
    run_id: str
    graph_id: str
    state: Dict[str, Any]
    logs: List[str]
    status: str