from typing import Dict, Any, List, Callable, Optional
from app.models import NodeDefinition, EdgeDefinition


class WorkflowGraph:
    def __init__(
        self,
        nodes: List[NodeDefinition],
        edges: List[EdgeDefinition],
        tool_registry: Dict[str, Callable]
    ):
        self.nodes = {node.name: node for node in nodes}
        self.edges = edges
        self.tool_registry = tool_registry
        self._validate()
    
    def _validate(self):
        """Validate graph structure"""
        # Check all tools exist
        for node in self.nodes.values():
            if node.tool not in self.tool_registry:
                raise ValueError(f"Tool '{node.tool}' not found in registry")
        
        # Check edge references
        for edge in self.edges:
            if edge.from_node not in self.nodes:
                raise ValueError(f"Node '{edge.from_node}' not found")
            if edge.to_node not in self.nodes:
                raise ValueError(f"Node '{edge.to_node}' not found")
    
    def get_start_node(self) -> str:
        """Get the starting node (node with no incoming edges)"""
        incoming = {edge.to_node for edge in self.edges}
        for node_name in self.nodes.keys():
            if node_name not in incoming:
                return node_name
        raise ValueError("No start node found")
    
    def get_next_nodes(self, current_node: str, state: Dict[str, Any]) -> List[str]:
        """Get next nodes based on edges and conditions"""
        next_nodes = []
        for edge in self.edges:
            if edge.from_node == current_node:
                if self._evaluate_condition(edge.condition, state):
                    next_nodes.append(edge.to_node)
        return next_nodes
    
    def _evaluate_condition(
        self,
        condition: Optional[Dict[str, Any]],
        state: Dict[str, Any]
    ) -> bool:
        """Evaluate edge condition"""
        if not condition:
            return True
        
        field = condition.get("field")
        operator = condition.get("operator")
        value = condition.get("value")
        
        if not all([field, operator]):
            return True
        
        state_value = state.get(field)
        
        if operator == ">=":
            return state_value >= value
        elif operator == "<=":
            return state_value <= value
        elif operator == ">":
            return state_value > value
        elif operator == "<":
            return state_value < value
        elif operator == "==":
            return state_value == value
        elif operator == "!=":
            return state_value != value
        
        return True