"""
Test OpenAI integration
"""

import pytest
from agentmind import Memory
from agentmind.integrations.openai import enhance_with_memory, create_memory_plugin


def test_enhance_with_memory():
    """Test enhancing messages with memory context"""
    memory = Memory(local_mode=True)
    
    # Add some memories
    memory.remember("User's name is John")
    memory.remember("User prefers Python programming")
    memory.remember("User is building an AI startup")
    
    # Test messages - use a query that will match
    messages = [
        {"role": "user", "content": "Tell me about the user"}
    ]
    
    # Enhance with memory
    enhanced = enhance_with_memory(messages, memory)
    
    # Should have system message with context
    assert len(enhanced) > len(messages)
    
    # Check for system message with context
    context_msg = None
    for msg in enhanced:
        if msg.get("role") == "system" and "Relevant context from memory:" in msg.get("content", ""):
            context_msg = msg
            break
    
    assert context_msg is not None
    assert "User's name is John" in context_msg["content"]


def test_enhance_with_specific_query():
    """Test enhancing with specific query"""
    memory = Memory(local_mode=True)
    
    memory.remember("User likes Python programming")
    memory.remember("User likes coffee")
    memory.remember("User has a dog named Max")
    
    messages = [
        {"role": "user", "content": "Tell me a joke"}
    ]
    
    # Query specifically about Python
    enhanced = enhance_with_memory(messages, memory, query="Python")
    
    # Should find Python-related memory
    context_found = False
    for msg in enhanced:
        if msg.get("role") == "system" and "Python" in msg.get("content", ""):
            context_found = True
            break
    
    assert context_found


def test_create_memory_plugin():
    """Test OpenAI function/plugin creation"""
    memory = Memory(local_mode=True)
    plugin = create_memory_plugin(memory)
    
    assert plugin["name"] == "remember"
    assert "parameters" in plugin
    assert "content" in plugin["parameters"]["properties"]


def test_empty_memory():
    """Test with empty memory"""
    memory = Memory(local_mode=True)
    
    messages = [
        {"role": "user", "content": "Hello"}
    ]
    
    enhanced = enhance_with_memory(messages, memory)
    
    # Should add system message even without memories
    assert len(enhanced) == 2  # Original message + system message
    assert any(msg.get("role") == "system" for msg in enhanced)