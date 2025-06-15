"""
Type definitions for AgentMind Memory
"""
from typing import Optional, Dict, Any, List, Literal
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class RecallStrategy(str, Enum):
    """Memory recall strategies"""
    SEMANTIC = "semantic"
    RECENCY = "recency"
    IMPORTANCE = "importance"
    HYBRID = "hybrid"


class MemoryConfig(BaseModel):
    """Configuration for Memory instance"""
    namespace: Optional[str] = Field(default="default", description="Memory namespace")
    retention_days: Optional[int] = Field(default=90, description="Days to retain memories")
    embedding_model: str = Field(default="text-embedding-ada-002", description="Embedding model")
    auto_summarize: bool = Field(default=True, description="Auto-summarize long sessions")
    encryption_key: Optional[str] = Field(default=None, description="Optional E2E encryption")


class MemoryMetadata(BaseModel):
    """Metadata for memory entries"""
    importance: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)
    confidence: Optional[float] = Field(default=1.0, ge=0.0, le=1.0)
    category: Optional[str] = None
    source: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    custom: Dict[str, Any] = Field(default_factory=dict)


class MemoryEntry(BaseModel):
    """A single memory entry"""
    id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: MemoryMetadata = Field(default_factory=MemoryMetadata)
    user_id: str
    session_id: Optional[str] = None
    timestamp: datetime
    ttl: Optional[int] = None
    relations: List[str] = Field(default_factory=list)


class RecallResult(BaseModel):
    """Result from memory recall"""
    memories: List[MemoryEntry]
    query: str
    strategy: RecallStrategy
    total_count: int
    relevance_scores: Optional[List[float]] = None


class MemoryStats(BaseModel):
    """Memory usage statistics"""
    total_memories: int
    total_users: int
    storage_used_mb: float
    recall_count_30d: int
    popular_categories: List[Dict[str, Any]]
    retention_rate: float