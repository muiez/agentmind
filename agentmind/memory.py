"""
Core Memory implementation for AgentMind
"""
import os
import json
import hashlib
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timedelta, timezone
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
        content: Any,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        ttl: Optional[int] = None,
        id: Optional[str] = None
    ) -> str:
        """
        Store a memory.
        
        Args:
            content: Any data to remember (string, dict, list, etc.)
            metadata: Optional metadata dict
            user_id: Optional user ID (defaults to namespace)
            session_id: Optional session ID
            ttl: Optional time-to-live in seconds
            id: Optional custom ID (auto-generated if not provided)
            
        Returns:
            str: The memory ID for later retrieval
        """
        # Create memory metadata
        if metadata:
            # Separate known fields from custom fields
            known_fields = {'importance', 'confidence', 'category', 'source', 'tags'}
            meta_dict = {}
            custom_fields = {}
            
            for key, value in metadata.items():
                if key in known_fields:
                    meta_dict[key] = value
                else:
                    custom_fields[key] = value
            
            if custom_fields:
                meta_dict['custom'] = custom_fields
                
            meta = MemoryMetadata(**meta_dict)
        else:
            meta = MemoryMetadata()
        
        # Generate memory ID
        if id:
            memory_id = id
        else:
            memory_id = self._generate_id(str(content), user_id)
        
        # Convert content to string if necessary for MemoryEntry
        # but store original content for retrieval
        content_str = json.dumps(content) if not isinstance(content, str) else content
        
        # Create memory entry
        entry = MemoryEntry(
            id=memory_id,
            content=content_str,
            metadata=meta,
            user_id=user_id or self.config.namespace,
            session_id=session_id,
            timestamp=datetime.now(timezone.utc),
            ttl=ttl
        )
        
        # Store via API (in production)
        # response = self._session.post(f"{self.base_url}/memories", json=entry.dict())
        # response.raise_for_status()
        
        # For MVP, store in local cache
        # Store both the entry and the original content
        self._cache[memory_id] = entry
        self._original_content = getattr(self, '_original_content', {})
        self._original_content[memory_id] = content
        
        return memory_id
    
    def remember_batch(
        self,
        memories: List[Union[str, Dict[str, Any]]],
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> List[str]:
        """Store multiple memories at once, returns list of memory IDs"""
        ids = []
        for memory in memories:
            if isinstance(memory, str):
                memory_id = self.remember(memory, user_id=user_id, session_id=session_id)
            else:
                memory_id = self.remember(
                    content=memory.get("content"),
                    metadata=memory.get("metadata"),
                    user_id=user_id or memory.get("user_id"),
                    session_id=session_id or memory.get("session_id"),
                    ttl=memory.get("ttl"),
                    id=memory.get("id")
                )
            ids.append(memory_id)
        return ids
    
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
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
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
                user_memories.append(entry.model_dump())
        
        return {
            "user_id": user_id,
            "export_date": datetime.now(timezone.utc).isoformat(),
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
                entry_dict = e.model_dump()
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
        unique_string = f"{content}{user_id or ''}{datetime.now(timezone.utc).isoformat()}"
        return f"mem_{hashlib.sha256(unique_string.encode()).hexdigest()[:12]}"
    
    def get(self, memory_id: str, include_metadata: bool = False) -> Any:
        """
        Retrieve memory by ID.
        
        Args:
            memory_id: The ID returned by remember() or custom ID
            include_metadata: Return metadata along with content
            
        Returns:
            The stored content (or dict with content + metadata)
            
        Raises:
            KeyError: If memory_id not found
        """
        if memory_id not in self._cache:
            # Suggest similar IDs if possible
            similar_ids = [id for id in self._cache.keys() if memory_id.lower() in id.lower()][:3]
            error_msg = f"Memory ID '{memory_id}' not found."
            if similar_ids:
                error_msg += f" Did you mean one of: {', '.join(similar_ids)}?"
            raise KeyError(error_msg)
        
        # Get original content if available
        original_content = getattr(self, '_original_content', {})
        if memory_id in original_content:
            content = original_content[memory_id]
        else:
            # Fall back to string content from entry
            entry = self._cache[memory_id]
            try:
                content = json.loads(entry.content)
            except:
                content = entry.content
        
        if include_metadata:
            entry = self._cache[memory_id]
            return {
                "content": content,
                "id": memory_id,
                "timestamp": entry.timestamp.isoformat(),
                "session_id": entry.session_id,
                "user_id": entry.user_id,
                "metadata": entry.metadata.model_dump(),
                "ttl": entry.ttl
            }
        
        return content
    
    def list(
        self,
        include_data: bool = False,
        limit: int = 100,
        offset: int = 0,
        **filters
    ) -> List[Dict[str, Any]]:
        """
        List all memories with their metadata.
        
        Args:
            include_data: Include full content (not just preview)
            limit: Maximum number of items to return
            offset: Skip this many items (for pagination)
            **filters: Filter by metadata (type, created_after, user_id, session_id, tags, etc.)
            
        Returns:
            List of memory summaries (or full data if requested)
        """
        memories = []
        
        # Apply filters
        filtered_entries = []
        for memory_id, entry in self._cache.items():
            # User filter
            if 'user_id' in filters and entry.user_id != filters['user_id']:
                continue
            
            # Session filter
            if 'session_id' in filters and entry.session_id != filters['session_id']:
                continue
            
            # Date filter
            if 'created_after' in filters:
                filter_date = datetime.fromisoformat(filters['created_after']) if isinstance(filters['created_after'], str) else filters['created_after']
                if entry.timestamp < filter_date:
                    continue
            
            # Category filter
            if 'category' in filters and entry.metadata.category != filters['category']:
                continue
            
            # Tags filter
            if 'tags' in filters:
                filter_tags = filters['tags'] if isinstance(filters['tags'], list) else [filters['tags']]
                if not any(tag in entry.metadata.tags for tag in filter_tags):
                    continue
            
            # Type filter (based on original content)
            if 'type' in filters:
                original_content = getattr(self, '_original_content', {})
                if memory_id in original_content:
                    content_type = type(original_content[memory_id]).__name__
                else:
                    content_type = 'str'
                
                if content_type != filters['type']:
                    continue
            
            filtered_entries.append((memory_id, entry))
        
        # Sort by timestamp (newest first)
        filtered_entries.sort(key=lambda x: x[1].timestamp, reverse=True)
        
        # Apply pagination
        paginated_entries = filtered_entries[offset:offset + limit]
        
        # Build response
        for memory_id, entry in paginated_entries:
            # Get content preview
            original_content = getattr(self, '_original_content', {})
            if memory_id in original_content:
                content = original_content[memory_id]
                content_type = type(content).__name__
            else:
                try:
                    content = json.loads(entry.content)
                    content_type = type(content).__name__
                except:
                    content = entry.content
                    content_type = 'str'
            
            # Create preview
            if isinstance(content, str):
                preview = content[:100] + "..." if len(content) > 100 else content
            elif isinstance(content, dict):
                preview = f"Dict with {len(content)} keys"
            elif isinstance(content, list):
                preview = f"List with {len(content)} items"
            else:
                preview = str(content)[:100] + "..." if len(str(content)) > 100 else str(content)
            
            # Calculate size
            size_str = json.dumps(content) if not isinstance(content, str) else content
            size_bytes = len(size_str.encode('utf-8'))
            if size_bytes < 1024:
                size = f"{size_bytes} bytes"
            elif size_bytes < 1024 * 1024:
                size = f"{size_bytes / 1024:.1f} KB"
            else:
                size = f"{size_bytes / 1024 / 1024:.1f} MB"
            
            memory_info = {
                "id": memory_id,
                "preview": preview,
                "type": content_type,
                "size": size,
                "created": entry.timestamp.isoformat(),
                "user_id": entry.user_id,
                "session_id": entry.session_id,
                "metadata": entry.metadata.model_dump()
            }
            
            if include_data:
                memory_info["content"] = content
            
            memories.append(memory_info)
        
        return memories
    
    def inspect(self, memory_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific memory.
        
        Args:
            memory_id: The memory ID to inspect
            
        Returns:
            Complete details including content, all metadata, and usage stats
            
        Raises:
            KeyError: If memory_id not found
        """
        if memory_id not in self._cache:
            raise KeyError(f"Memory ID '{memory_id}' not found")
        
        entry = self._cache[memory_id]
        
        # Get original content
        original_content = getattr(self, '_original_content', {})
        if memory_id in original_content:
            content = original_content[memory_id]
            content_type = type(content).__name__
        else:
            try:
                content = json.loads(entry.content)
                content_type = type(content).__name__
            except:
                content = entry.content
                content_type = 'str'
        
        # Calculate size
        size_str = json.dumps(content) if not isinstance(content, str) else content
        size_bytes = len(size_str.encode('utf-8'))
        if size_bytes < 1024:
            size = f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            size = f"{size_bytes / 1024:.1f} KB"
        else:
            size = f"{size_bytes / 1024 / 1024:.1f} MB"
        
        # TODO: In production, track access count and last accessed
        return {
            "id": memory_id,
            "content": content,
            "metadata": {
                "type": content_type,
                "size": size,
                "created": entry.timestamp.isoformat(),
                "last_accessed": entry.timestamp.isoformat(),  # Would track separately in production
                "access_count": 1,  # Would track in production
                "session_id": entry.session_id,
                "user_id": entry.user_id,
                "tags": entry.metadata.tags,
                "category": entry.metadata.category,
                "importance": entry.metadata.importance,
                "confidence": entry.metadata.confidence,
                "ttl": entry.ttl,
                "custom": entry.metadata.custom
            }
        }
    
    def exists(self, memory_id: str) -> bool:
        """
        Check if a memory ID exists.
        
        Args:
            memory_id: The memory ID to check
            
        Returns:
            True if exists, False otherwise
        """
        return memory_id in self._cache
    
    def delete(self, memory_id: str) -> bool:
        """
        Delete a memory by ID.
        
        Args:
            memory_id: The memory ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        if memory_id in self._cache:
            del self._cache[memory_id]
            
            # Also remove from original content cache
            original_content = getattr(self, '_original_content', {})
            if memory_id in original_content:
                del original_content[memory_id]
            
            return True
        return False