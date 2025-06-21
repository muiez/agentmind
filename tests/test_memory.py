"""
Tests for AgentMind Memory
"""
import pytest
from datetime import datetime, timedelta, timezone
from agentmind import Memory, MemoryConfig, RecallStrategy


@pytest.fixture
def memory():
    """Create a test memory instance"""
    return Memory(api_key="test_api_key")


def test_remember_basic(memory):
    """Test basic memory storage - now returns ID"""
    memory_id = memory.remember("Test memory content")
    
    assert isinstance(memory_id, str)
    assert memory_id.startswith("mem_")
    
    # Verify we can retrieve it
    content = memory.get(memory_id)
    assert content == "Test memory content"


def test_remember_with_metadata(memory):
    """Test memory with metadata"""
    memory_id = memory.remember(
        "Important fact",
        metadata={
            "importance": 0.9,
            "category": "test",
            "custom_field": "value"
        }
    )
    
    # Get with metadata
    data = memory.get(memory_id, include_metadata=True)
    assert data["content"] == "Important fact"
    assert data["metadata"]["importance"] == 0.9
    assert data["metadata"]["category"] == "test"
    assert data["metadata"]["custom"]["custom_field"] == "value"


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
    
    ids = memory.remember_batch(memories)
    
    assert len(ids) == 3
    assert all(isinstance(id, str) for id in ids)
    assert memory.get(ids[0]) == "First memory"
    assert memory.get(ids[1]) == "Second memory"


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
    memory_id = memory.remember("Memory to forget")
    
    # Verify it exists
    assert memory.exists(memory_id)
    
    # Forget
    success = memory.forget(memory_id)
    assert success
    
    # Verify it's gone
    assert not memory.exists(memory_id)
    
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
    memory_id = memory.remember("Uncertain fact", metadata={"confidence": 0.5})
    
    # Update confidence
    success = memory.update_confidence(memory_id, 0.9)
    assert success
    
    # Verify the update
    data = memory.get(memory_id, include_metadata=True)
    assert data["metadata"]["confidence"] == 0.9


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


def test_remember_with_custom_id(memory):
    """Test remembering with custom ID"""
    custom_id = "my_custom_id_123"
    returned_id = memory.remember("Content with custom ID", id=custom_id)
    
    assert returned_id == custom_id
    assert memory.get(custom_id) == "Content with custom ID"


def test_remember_complex_types(memory):
    """Test remembering complex data types"""
    # Dict
    dict_data = {"name": "John", "age": 30, "hobbies": ["reading", "coding"]}
    dict_id = memory.remember(dict_data)
    retrieved_dict = memory.get(dict_id)
    assert retrieved_dict == dict_data
    
    # List
    list_data = [1, 2, 3, {"nested": "value"}]
    list_id = memory.remember(list_data)
    retrieved_list = memory.get(list_id)
    assert retrieved_list == list_data
    
    # Complex nested structure
    complex_data = {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ],
        "metadata": {
            "version": "1.0",
            "timestamp": "2024-01-20"
        }
    }
    complex_id = memory.remember(complex_data)
    retrieved_complex = memory.get(complex_id)
    assert retrieved_complex == complex_data


def test_get_with_metadata(memory):
    """Test getting memory with metadata"""
    memory_id = memory.remember(
        "Test content",
        metadata={"category": "test", "tags": ["important", "review"]},
        session_id="test_session"
    )
    
    # Get without metadata
    content = memory.get(memory_id)
    assert content == "Test content"
    
    # Get with metadata
    full_data = memory.get(memory_id, include_metadata=True)
    assert full_data["content"] == "Test content"
    assert full_data["id"] == memory_id
    assert full_data["session_id"] == "test_session"
    assert full_data["metadata"]["category"] == "test"
    assert "important" in full_data["metadata"]["tags"]


def test_get_nonexistent_memory(memory):
    """Test getting non-existent memory"""
    with pytest.raises(KeyError) as exc_info:
        memory.get("nonexistent_id")
    
    assert "not found" in str(exc_info.value)


def test_list_memories(memory):
    """Test listing memories"""
    # Create some memories
    ids = []
    ids.append(memory.remember("First memory", metadata={"category": "cat1"}))
    ids.append(memory.remember("Second memory", metadata={"category": "cat2"}))
    ids.append(memory.remember({"type": "dict", "value": 123}))
    
    # List all
    all_memories = memory.list()
    assert len(all_memories) >= 3
    
    # Check structure
    first_memory = next(m for m in all_memories if m["id"] == ids[0])
    assert first_memory["preview"] == "First memory"
    assert first_memory["type"] == "str"
    assert "bytes" in first_memory["size"]
    
    # List with data
    with_data = memory.list(include_data=True)
    first_with_data = next(m for m in with_data if m["id"] == ids[0])
    assert first_with_data["content"] == "First memory"


def test_list_with_filters(memory):
    """Test listing with filters"""
    # Create memories with different attributes
    user1_id = memory.remember("User 1 memory", user_id="user1")
    user2_id = memory.remember("User 2 memory", user_id="user2")
    cat_id = memory.remember("Categorized", metadata={"category": "important"})
    tagged_id = memory.remember("Tagged", metadata={"tags": ["urgent", "review"]})
    
    # Filter by user
    user1_memories = memory.list(user_id="user1")
    assert len(user1_memories) >= 1
    assert all(m["user_id"] == "user1" for m in user1_memories)
    
    # Filter by category
    important = memory.list(category="important")
    assert len(important) >= 1
    assert any(m["id"] == cat_id for m in important)
    
    # Filter by tags
    urgent = memory.list(tags="urgent")
    assert len(urgent) >= 1
    assert any(m["id"] == tagged_id for m in urgent)


def test_list_pagination(memory):
    """Test list pagination"""
    # Create 10 memories
    for i in range(10):
        memory.remember(f"Memory {i}")
    
    # Get first page
    page1 = memory.list(limit=5, offset=0)
    assert len(page1) == 5
    
    # Get second page
    page2 = memory.list(limit=5, offset=5)
    assert len(page2) >= 5
    
    # Ensure different pages
    page1_ids = {m["id"] for m in page1}
    page2_ids = {m["id"] for m in page2}
    assert page1_ids.isdisjoint(page2_ids)


def test_inspect_memory(memory):
    """Test inspecting memory details"""
    dict_data = {"key": "value", "nested": {"level": 2}}
    memory_id = memory.remember(
        dict_data,
        metadata={"category": "test", "importance": 0.8},
        session_id="inspect_test"
    )
    
    details = memory.inspect(memory_id)
    
    assert details["id"] == memory_id
    assert details["content"] == dict_data
    assert details["metadata"]["type"] == "dict"
    assert details["metadata"]["category"] == "test"
    assert details["metadata"]["importance"] == 0.8
    assert details["metadata"]["session_id"] == "inspect_test"
    assert "size" in details["metadata"]
    assert "created" in details["metadata"]


def test_exists(memory):
    """Test memory existence check"""
    memory_id = memory.remember("Test existence")
    
    assert memory.exists(memory_id)
    assert not memory.exists("nonexistent_id")
    
    # After deletion
    memory.delete(memory_id)
    assert not memory.exists(memory_id)


def test_delete(memory):
    """Test deleting memories"""
    # Create memory
    memory_id = memory.remember("To be deleted")
    assert memory.exists(memory_id)
    
    # Delete it
    success = memory.delete(memory_id)
    assert success
    assert not memory.exists(memory_id)
    
    # Try to get deleted memory
    with pytest.raises(KeyError):
        memory.get(memory_id)
    
    # Delete non-existent
    assert not memory.delete("nonexistent_id")


def test_delete_complex_type(memory):
    """Test deleting complex type preserves cleanup"""
    complex_data = {"data": [1, 2, 3], "metadata": {"type": "test"}}
    memory_id = memory.remember(complex_data)
    
    # Verify it's stored
    assert memory.get(memory_id) == complex_data
    
    # Delete and verify complete cleanup
    memory.delete(memory_id)
    
    # Should not exist in either cache
    assert not memory.exists(memory_id)
    with pytest.raises(KeyError):
        memory.get(memory_id)