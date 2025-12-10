from typing import Dict, Any, Optional


class MemoryStore:
    """Simple in-memory storage"""
    
    def __init__(self):
        self._store: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any):
        """Store a value"""
        self._store[key] = value
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value"""
        return self._store.get(key)
    
    def delete(self, key: str):
        """Delete a value"""
        if key in self._store:
            del self._store[key]
    
    def list_keys(self) -> list:
        """List all keys"""
        return list(self._store.keys())