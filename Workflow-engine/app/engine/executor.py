from typing import Dict, Any, List, Tuple
from app.engine.graph import WorkflowGraph
import asyncio


class GraphExecutor:
    def __init__(self, graph: WorkflowGraph, max_iterations: int = 100):
        self.graph = graph
        self.max_iterations = max_iterations
    
    async def execute(
        self,
        initial_state: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Execute the workflow graph"""
        state = initial_state.copy()
        logs = []
        visited = set()
        iteration = 0
        
        current_node = self.graph.get_start_node()
        logs.append(f"Starting execution from node: {current_node}")
        
        while current_node and iteration < self.max_iterations:
            iteration += 1
            
            # Execute current node
            node_def = self.graph.nodes[current_node]
            tool = self.graph.tool_registry[node_def.tool]
            
            logs.append(f"Executing node: {current_node} with tool: {node_def.tool}")
            
            try:
                result = await self._execute_tool(tool, state)
                state.update(result)
                logs.append(f"Node {current_node} completed successfully")
            except Exception as e:
                logs.append(f"Error in node {current_node}: {str(e)}")
                raise
            
            # Check node condition (for loops)
            if node_def.condition:
                if not self.graph._evaluate_condition(node_def.condition, state):
                    logs.append(f"Node condition not met, continuing to next node")
            
            # Get next nodes
            next_nodes = self.graph.get_next_nodes(current_node, state)
            
            if not next_nodes:
                logs.append("No more nodes to execute. Workflow complete.")
                break
            
            # Simple strategy: take first valid next node
            current_node = next_nodes[0]
        
        if iteration >= self.max_iterations:
            logs.append(f"Warning: Max iterations ({self.max_iterations}) reached")
        
        logs.append(f"Execution completed in {iteration} iterations")
        return state, logs
    
    async def _execute_tool(
        self,
        tool: callable,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool function"""
        if asyncio.iscoroutinefunction(tool):
            return await tool(state)
        else:
            return tool(state)