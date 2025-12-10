from typing import Dict, Any
import re


def register_code_review_tools(registry: Dict[str, callable]):
    """Register all code review tools"""
    registry["extract_functions"] = extract_functions
    registry["check_complexity"] = check_complexity
    registry["detect_issues"] = detect_issues
    registry["suggest_improvements"] = suggest_improvements


def extract_functions(state: Dict[str, Any]) -> Dict[str, Any]:
    """Extract functions from code"""
    code = state.get("code", "")
    
    # Simple function extraction using regex
    pattern = r'def\s+(\w+)\s*\([^)]*\):'
    functions = re.findall(pattern, code)
    
    return {
        "functions": functions,
        "function_count": len(functions)
    }


def check_complexity(state: Dict[str, Any]) -> Dict[str, Any]:
    """Check code complexity"""
    code = state.get("code", "")
    functions = state.get("functions", [])
    
    # Simple complexity metrics
    lines = code.split("\n")
    complexity_score = 0
    
    # Count control structures
    for line in lines:
        if any(keyword in line for keyword in ["if", "for", "while", "try"]):
            complexity_score += 1
    
    return {
        "complexity_score": complexity_score,
        "is_complex": complexity_score > 10
    }


def detect_issues(state: Dict[str, Any]) -> Dict[str, Any]:
    """Detect basic code issues"""
    code = state.get("code", "")
    issues = []
    
    lines = code.split("\n")
    
    for i, line in enumerate(lines, 1):
        # Check for common issues
        if len(line) > 100:
            issues.append(f"Line {i}: Line too long ({len(line)} chars)")
        
        if "TODO" in line or "FIXME" in line:
            issues.append(f"Line {i}: Contains TODO/FIXME comment")
        
        if "print(" in line and "def " not in line:
            issues.append(f"Line {i}: Contains print statement")
    
    return {
        "issues": issues,
        "issue_count": len(issues),
        "quality_score": max(0, 100 - len(issues) * 5)
    }


def suggest_improvements(state: Dict[str, Any]) -> Dict[str, Any]:
    """Suggest code improvements"""
    issues = state.get("issues", [])
    complexity_score = state.get("complexity_score", 0)
    
    suggestions = []
    
    if complexity_score > 10:
        suggestions.append("Consider breaking down complex functions")
    
    if len(issues) > 5:
        suggestions.append("Address code quality issues")
    
    if state.get("function_count", 0) == 0:
        suggestions.append("Consider adding functions for better structure")
    
    return {
        "suggestions": suggestions,
        "improvement_needed": len(suggestions) > 0
    }