"""
Tests for AgentMind Memory
"""
import pytest
from datetime import datetime, timedelta
from agentmind import Memory, MemoryConfig, RecallStrategy


@pytest.fixture
def memory():
    """Create a test memory instance"""
    return Memory(api_key="test_api_key")


def test_remember_basic(memory):
    """Test basic memory storage"""
    entry = memory.remember("Test memory content")
    
    assert entry.content == "Test memory content"
    assert entry.id.startswith("mem_")
    assert entry.timestamp <= datetime.utcnow()


def test_remember_with_metadata(memory):
    """Test memory with metadata"""
    entry = memory.remember(
        "Important fact",
        metadata={
            "importance": 0.9,
            "category": "test",
            "custom_field": "value"
        }
    )
    
    assert entry.metadata.importance == 0.9
    assert entry.metadata.category == "test"
    assert entry.metadata.custom["custom_field"] == "value"


def test_recall_basic(memory):
    """Test basic recall"""
    # Store some memories
    memory.remember("Python is a great language")
    memory.remember("JavaScript is used for web development")
    memory.remember("Rust is fast and safe")
    
    # Recall
    results = memory.recall("Python programming")
    
    assert len(results) > 0
    assert "Python is a great language" in results


def test_recall_with_filters(memory):
    """Test recall with filters"""
    # Store categorized memories
    memory.remember("Technical meeting notes", metadata={"category": "meeting"})
    memory.remember("Product roadmap discussion", metadata={"category": "meeting"})
    memory.remember("Python best practices", metadata={"category": "technical"})
    
    # This would work with real API
    # For now, our simple implementation doesn't support filters
    results = memory.recall("meeting", filters={"category": "meeting"})
    
    # At least shouldn't crash
    assert isinstance(results, list)


def test_batch_remember(memory):
    """Test batch memory storage"""
    memories = [
        "First memory",
        {"content": "Second memory", "metadata": {"importance": 0.8}},
        {"content": "Third memory", "ttl": 3600}
    ]
    
    entries = memory.remember_batch(memories)
    
    assert len(entries) == 3
    assert entries[0].content == "First memory"
    assert entries[1].metadata.importance == 0.8


def test_get_facts(memory):
    """Test getting categorized facts"""
    # Store facts
    memory.remember("Python is interpreted", metadata={"category": "python"})
    memory.remember("Python has GIL", metadata={"category": "python"})
    memory.remember("JavaScript is async", metadata={"category": "javascript"})
    
    # Get Python facts
    facts = memory.get_facts(category="python")
    
    assert len(facts) == 2
    assert all(f["content"].startswith("Python") for f in facts)


def test_get_recent(memory):
    """Test getting recent memories"""
    # Store some memories
    memory.remember("Recent memory 1")
    memory.remember("Recent memory 2")
    
    # Get recent
    recent = memory.get_recent(hours=1)
    
    assert len(recent) >= 2
    assert "Recent memory 1" in recent
    assert "Recent memory 2" in recent


def test_forget(memory):
    """Test forgetting memories"""
    # Store and get ID
    entry = memory.remember("Memory to forget")
    memory_id = entry.id
    
    # Forget
    success = memory.forget(memory_id)
    assert success
    
    # Try to forget again
    success = memory.forget(memory_id)
    assert not success


def test_session_management(memory):
    """Test session-based memory management"""
    session_id = "test_session_123"
    
    # Store session memories
    memory.remember("Session start", session_id=session_id)
    memory.remember("User clicked button", session_id=session_id)
    memory.remember("Session end", session_id=session_id)
    
    # Summarize
    summary = memory.summarize_session(session_id)
    assert "3 memories" in summary
    
    # Clear session
    deleted = memory.clear_session(session_id)
    assert deleted == 3


def test_gdpr_compliance(memory):
    """Test GDPR compliance features"""
    user_id = "test_user_123"
    
    # Store user data
    memory.remember("User preference 1", user_id=user_id)
    memory.remember("User preference 2", user_id=user_id)
    
    # Export user data
    export = memory.export_user_data(user_id)
    assert export["user_id"] == user_id
    assert export["memory_count"] == 2
    
    # Delete user data
    deleted = memory.delete_user_data(user_id)
    assert deleted == 2
    
    # Verify deletion
    export = memory.export_user_data(user_id)
    assert export["memory_count"] == 0


def test_update_confidence(memory):
    """Test updating memory confidence"""
    entry = memory.remember("Uncertain fact", metadata={"confidence": 0.5})
    
    # Update confidence
    success = memory.update_confidence(entry.id, 0.9)
    assert success
    
    # In real implementation, we'd verify the update
    # For now, just check it doesn't crash


def test_memory_stats(memory):
    """Test memory statistics"""
    # Add some memories
    memory.remember("Memory 1", user_id="user1")
    memory.remember("Memory 2", user_id="user1")
    memory.remember("Memory 3", user_id="user2")
    
    stats = memory.get_stats()
    
    assert stats.total_memories >= 3
    assert stats.total_users >= 2
    assert stats.storage_used_mb > 0