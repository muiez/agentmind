"""
Core Memory implementation for AgentMind
"""
import os
import json
import hashlib
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timedelta
import requests
from .types import (
    MemoryConfig, RecallStrategy, MemoryEntry, 
    RecallResult, MemoryMetadata, MemoryStats
)


class Memory:
    """
    The core Memory class for AgentMind.
    
    Example:
        memory = Memory(api_key="am_live_xxx")
        memory.remember("User likes Python")
        context = memory.recall("programming preferences")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        config: Optional[MemoryConfig] = None,
        base_url: str = "https://api.agentmind.ai/v1",
        local_mode: bool = False
    ):
        """
        Initialize Memory instance.
        
        Args:
            api_key: API key for hosted service (required unless local_mode=True)
            config: Memory configuration
            base_url: API base URL for hosted service
            local_mode: If True, use local storage only (no API calls)
        """
        self.local_mode = local_mode
        self.config = config or MemoryConfig()
        
        if not local_mode:
            # Hosted mode - requires API key
            self.api_key = api_key or os.getenv("AGENTMIND_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "API key required for hosted mode. "
                    "Set AGENTMIND_API_KEY, pass api_key, or use local_mode=True"
                )
            
            # Import here to avoid circular dependency
            from .client import APIClient
            self.client = APIClient(self.api_key, base_url)
        else:
            # Local mode - no API needed
            self.api_key = None
            self.client = None
        
        # Local cache (used in both modes)
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes
    
    def remember(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        ttl: Optional[int] = None
    ) -> MemoryEntry:
        """
        Store a memory.
        
        Args:
            content: The content to remember
            metadata: Optional metadata dict
            user_id: Optional user ID (defaults to namespace)
            session_id: Optional session ID
            ttl: Optional time-to-live in seconds
            
        Returns:
            MemoryEntry: The stored memory
        """
        # Create memory metadata
        meta = MemoryMetadata(**(metadata or {}))
        
        # Generate memory ID
        memory_id = self._generate_id(content, user_id)
        
        # Create memory entry
        entry = MemoryEntry(
            id=memory_id,
            content=content,
            metadata=meta,
            user_id=user_id or self.config.namespace,
            session_id=session_id,
            timestamp=datetime.utcnow(),
            ttl=ttl
        )
        
        # Store via API (in production)
        # response = self._session.post(f"{self.base_url}/memories", json=entry.dict())
        # response.raise_for_status()
        
        # For MVP, store in local cache
        self._cache[memory_id] = entry
        
        return entry
    
    def remember_batch(
        self,
        memories: List[Union[str, Dict[str, Any]]],
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> List[MemoryEntry]:
        """Store multiple memories at once"""
        entries = []
        for memory in memories:
            if isinstance(memory, str):
                entry = self.remember(memory, user_id=user_id, session_id=session_id)
            else:
                entry = self.remember(
                    content=memory.get("content"),
                    metadata=memory.get("metadata"),
                    user_id=user_id or memory.get("user_id"),
                    session_id=session_id or memory.get("session_id"),
                    ttl=memory.get("ttl")
                )
            entries.append(entry)
        return entries
    
    def recall(
        self,
        query: str,
        strategy: RecallStrategy = RecallStrategy.HYBRID,
        limit: int = 5,
        user_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Recall relevant memories.
        
        Args:
            query: The query to search for
            strategy: Recall strategy (semantic, recency, importance, hybrid)
            limit: Maximum number of memories to return
            user_id: Optional user filter
            filters: Optional metadata filters
            
        Returns:
            List of relevant memory contents
        """
        # In production, this would call the API
        # response = self._session.post(
        #     f"{self.base_url}/recall",
        #     json={
        #         "query": query,
        #         "strategy": strategy.value,
        #         "limit": limit,
        #         "user_id": user_id or self.config.namespace,
        #         "filters": filters
        #     }
        # )
        
        # For MVP, simple local search with improved matching
        results = []
        query_words = query.lower().split()
        
        for memory_id, entry in self._cache.items():
            if user_id and entry.user_id != user_id:
                continue
            
            # Check if any query word appears in the content
            content_lower = entry.content.lower()
            if any(word in content_lower for word in query_words):
                results.append(entry.content)
            
            # Also check metadata category if it exists
            if filters and 'category' in filters:
                if entry.metadata.category == filters['category']:
                    if entry.content not in results:
                        results.append(entry.content)
            
            if len(results) >= limit:
                break
        
        return results
    
    def get_facts(self, category: Optional[str] = None, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get structured facts from memory"""
        facts = []
        for memory_id, entry in self._cache.items():
            if user_id and entry.user_id != user_id:
                continue
            if category and entry.metadata.category != category:
                continue
            
            facts.append({
                "content": entry.content,
                "confidence": entry.metadata.confidence,
                "timestamp": entry.timestamp.isoformat()
            })
        
        return facts
    
    def get_recent(self, hours: int = 24, user_id: Optional[str] = None) -> List[str]:
        """Get recent memories"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent = []
        
        for memory_id, entry in self._cache.items():
            if user_id and entry.user_id != user_id:
                continue
            if entry.timestamp >= cutoff:
                recent.append(entry.content)
        
        return sorted(recent, key=lambda x: x, reverse=True)
    
    def forget(self, memory_id: str) -> bool:
        """Delete a specific memory"""
        if memory_id in self._cache:
            del self._cache[memory_id]
            return True
        return False
    
    def forget_before(self, date: Union[str, datetime], user_id: Optional[str] = None) -> int:
        """Delete memories before a certain date"""
        if isinstance(date, str):
            date = datetime.fromisoformat(date)
        
        to_delete = []
        for memory_id, entry in self._cache.items():
            if user_id and entry.user_id != user_id:
                continue
            if entry.timestamp < date:
                to_delete.append(memory_id)
        
        for memory_id in to_delete:
            del self._cache[memory_id]
        
        return len(to_delete)
    
    def update_confidence(self, memory_id: str, confidence: float) -> bool:
        """Update memory confidence score"""
        if memory_id in self._cache:
            self._cache[memory_id].metadata.confidence = confidence
            return True
        return False
    
    def summarize_session(self, session_id: str) -> str:
        """Summarize a session's memories"""
        session_memories = []
        for memory_id, entry in self._cache.items():
            if entry.session_id == session_id:
                session_memories.append(entry.content)
        
        if not session_memories:
            return "No memories found for session"
        
        # In production, this would use LLM for summarization
        summary = f"Session summary ({len(session_memories)} memories): "
        summary += "; ".join(session_memories[:3])
        if len(session_memories) > 3:
            summary += f"... and {len(session_memories) - 3} more"
        
        return summary
    
    def clear_session(self, session_id: str) -> int:
        """Clear all memories from a session"""
        to_delete = []
        for memory_id, entry in self._cache.items():
            if entry.session_id == session_id:
                to_delete.append(memory_id)
        
        for memory_id in to_delete:
            del self._cache[memory_id]
        
        return len(to_delete)
    
    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """Export all user data (GDPR compliance)"""
        user_memories = []
        for memory_id, entry in self._cache.items():
            if entry.user_id == user_id:
                user_memories.append(entry.dict())
        
        return {
            "user_id": user_id,
            "export_date": datetime.utcnow().isoformat(),
            "memory_count": len(user_memories),
            "memories": user_memories
        }
    
    def delete_user_data(self, user_id: str) -> int:
        """Delete all user data (GDPR right to erasure)"""
        to_delete = []
        for memory_id, entry in self._cache.items():
            if entry.user_id == user_id:
                to_delete.append(memory_id)
        
        for memory_id in to_delete:
            del self._cache[memory_id]
        
        return len(to_delete)
    
    def get_stats(self) -> MemoryStats:
        """Get memory usage statistics"""
        users = set()
        categories = {}
        
        for entry in self._cache.values():
            users.add(entry.user_id)
            if entry.metadata.category:
                categories[entry.metadata.category] = categories.get(entry.metadata.category, 0) + 1
        
        # Calculate approximate storage size
        try:
            # Convert entries to JSON-serializable format
            entries_data = []
            for e in self._cache.values():
                entry_dict = e.dict()
                # Convert datetime to string
                entry_dict['timestamp'] = entry_dict['timestamp'].isoformat()
                entries_data.append(entry_dict)
            storage_size = len(json.dumps(entries_data)) / 1024 / 1024
        except:
            storage_size = len(str(self._cache)) / 1024 / 1024
        
        return MemoryStats(
            total_memories=len(self._cache),
            total_users=len(users),
            storage_used_mb=storage_size,
            recall_count_30d=0,  # Would track in production
            popular_categories=[{"name": k, "count": v} for k, v in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]],
            retention_rate=1.0  # Would calculate in production
        )
    
    def _generate_id(self, content: str, user_id: Optional[str] = None) -> str:
        """Generate unique memory ID"""
        unique_string = f"{content}{user_id or ''}{datetime.utcnow().isoformat()}"
        return f"mem_{hashlib.sha256(unique_string.encode()).hexdigest()[:12]}"