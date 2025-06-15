"""
OpenAI integration for AgentMind
Enhance OpenAI chat completions with memory
"""

from typing import List, Dict, Any, Optional
from ..memory import Memory


def enhance_with_memory(
    messages: List[Dict[str, str]], 
    memory: Memory,
    max_context: int = 5,
    query: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Enhance OpenAI messages with relevant memory context
    
    Args:
        messages: List of OpenAI message dicts
        memory: AgentMind Memory instance
        max_context: Maximum number of memories to include
        query: Optional specific query for memory recall. If None, uses last user message
        
    Returns:
        Enhanced messages list with memory context injected
    """
    # Get the query from the last user message if not provided
    if query is None:
        user_messages = [msg for msg in messages if msg.get("role") == "user"]
        if user_messages:
            query = user_messages[-1].get("content", "")
        else:
            query = ""
    
    # Recall relevant memories
    if max_context > 0 and query:
        memories = memory.recall(query)[:max_context]
    else:
        memories = []
    
    if not memories:
        # Still add system message even without memories
        enhanced_messages = []
        has_system = any(msg.get("role") == "system" for msg in messages)
        if not has_system:
            enhanced_messages.append({
                "role": "system",
                "content": "You are a helpful assistant with access to conversation memory."
            })
        enhanced_messages.extend(messages)
        return enhanced_messages
    
    # Create context message
    context_content = "Relevant context from memory:\n"
    for i, mem in enumerate(memories, 1):
        context_content += f"{i}. {mem}\n"
    
    # Create a new messages list with context injected
    enhanced_messages = []
    
    # Add system message if not present
    has_system = any(msg.get("role") == "system" for msg in messages)
    if not has_system:
        enhanced_messages.append({
            "role": "system",
            "content": "You are a helpful assistant with access to conversation memory."
        })
    
    # Add existing messages, injecting context before the last user message
    for i, msg in enumerate(messages):
        if msg.get("role") == "user" and i == len(messages) - 1:
            # Inject context before the last user message
            enhanced_messages.append({
                "role": "system",
                "content": context_content
            })
        enhanced_messages.append(msg)
    
    return enhanced_messages


def create_memory_plugin(memory: Memory) -> Dict[str, Any]:
    """
    Create an OpenAI function/plugin that can store memories
    
    Args:
        memory: AgentMind Memory instance
        
    Returns:
        OpenAI function definition for memory storage
    """
    return {
        "name": "remember",
        "description": "Store important information in long-term memory",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The information to remember"
                },
                "metadata": {
                    "type": "object",
                    "description": "Optional metadata about the memory",
                    "properties": {
                        "importance": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "Importance level of the memory"
                        },
                        "category": {
                            "type": "string",
                            "description": "Category of the memory"
                        }
                    }
                }
            },
            "required": ["content"]
        }
    }


class OpenAIMemoryWrapper:
    """
    Wrapper class for OpenAI client with automatic memory management
    """
    
    def __init__(self, openai_client, memory: Memory):
        """
        Initialize wrapper
        
        Args:
            openai_client: OpenAI client instance
            memory: AgentMind Memory instance
        """
        self.client = openai_client
        self.memory = memory
        
    def create_completion(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """
        Create chat completion with automatic memory enhancement
        
        Args:
            messages: List of message dicts
            **kwargs: Additional arguments for OpenAI API
            
        Returns:
            OpenAI completion response
        """
        # Enhance messages with memory
        enhanced_messages = enhance_with_memory(messages, self.memory)
        
        # Make API call
        response = self.client.chat.completions.create(
            messages=enhanced_messages,
            **kwargs
        )
        
        # Store the interaction in memory
        if messages:
            last_user_msg = next((msg for msg in reversed(messages) if msg.get("role") == "user"), None)
            if last_user_msg:
                self.memory.remember(f"User asked: {last_user_msg.get('content', '')}")
            
        if response.choices and response.choices[0].message:
            assistant_response = response.choices[0].message.content
            self.memory.remember(f"Assistant responded: {assistant_response}")
            
        return response