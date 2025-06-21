"""
Basic usage example for AgentMind Memory
"""
import os
from agentmind import Memory, RecallStrategy

# Initialize memory (set AGENTMIND_API_KEY environment variable)
# For demo purposes, we'll use a mock API key
memory = Memory(api_key="am_demo_key_xxx")

def demo_basic_usage():
    """Demonstrate basic memory operations"""
    print("=== AgentMind Memory Demo ===\n")
    
    # Store some memories - now returns IDs
    print("1. Storing memories...")
    pref_id = memory.remember("User prefers Python for backend development", metadata={"category": "tech_preference"})
    exp_id = memory.remember("User mentioned they have expertise in ML compilers", metadata={"importance": 0.9})
    meeting_id = memory.remember("Meeting scheduled for next Tuesday at 3pm", id="tuesday_meeting")
    print(f"✓ Stored 3 memories with IDs: {pref_id[:12]}..., {exp_id[:12]}..., tuesday_meeting\n")
    
    # Direct retrieval by ID
    print("2. Direct memory access...")
    meeting = memory.get("tuesday_meeting")
    print(f"Retrieved by ID: {meeting}")
    
    # Get with metadata
    full_data = memory.get(pref_id, include_metadata=True)
    print(f"With metadata: Category={full_data['metadata']['category']}\n")
    
    # List all memories
    print("3. Exploring memory contents...")
    memories = memory.list(limit=5)
    for mem in memories:
        print(f"  - {mem['id'][:12]}...: {mem['preview']} ({mem['size']})")
    print()
    
    # Semantic recall still works
    print("4. Semantic search...")
    context = memory.recall("What programming language does the user prefer?")
    print(f"Query: 'What programming language does the user prefer?'")
    print(f"Results: {context}\n")
    
    # Inspect a specific memory
    print("5. Inspecting memory details...")
    details = memory.inspect(exp_id)
    print(f"Memory type: {details['metadata']['type']}")
    print(f"Size: {details['metadata']['size']}")
    print(f"Importance: {details['metadata']['importance']}\n")
    
    # Check existence and delete
    print("6. Memory lifecycle...")
    temp_id = memory.remember("Temporary note", id="temp_note")
    print(f"Exists? {memory.exists('temp_note')}")
    memory.delete("temp_note")
    print(f"After deletion: {memory.exists('temp_note')}\n")
    
    # Show statistics
    print("7. Memory statistics...")
    stats = memory.get_stats()
    print(f"Total memories: {stats.total_memories}")
    print(f"Storage used: {stats.storage_used_mb:.2f} MB\n")


def demo_advanced_features():
    """Demonstrate advanced memory features"""
    print("=== Advanced Features ===\n")
    
    # Store complex data types
    print("1. Storing complex data...")
    config_data = {
        "database": {"host": "localhost", "port": 5432},
        "cache": {"ttl": 3600, "max_size": "1GB"},
        "features": ["auth", "api", "webhooks"]
    }
    config_id = memory.remember(config_data, id="app_config")
    
    # Retrieve complex data
    retrieved_config = memory.get("app_config")
    print(f"Retrieved config: {retrieved_config['database']['host']}")
    print(f"Features: {', '.join(retrieved_config['features'])}\n")
    
    # Batch operations - returns list of IDs
    print("2. Batch memory storage...")
    memories = [
        {"content": "Q1 revenue: $50k", "metadata": {"category": "business", "importance": 0.8}},
        {"content": "Q2 target: $150k", "metadata": {"category": "business", "importance": 0.9}, "id": "q2_target"},
        {"content": "Hired first engineer", "metadata": {"category": "team", "importance": 0.9}}
    ]
    memory_ids = memory.remember_batch(memories, user_id="founder_001")
    print(f"✓ Stored batch of 3 memories with IDs: {[id[:12] + '...' if len(id) > 12 else id for id in memory_ids]}\n")
    
    # Filtering and exploring memories
    print("3. Filtering memories...")
    
    # List by category
    business_memories = memory.list(category="business")
    print(f"Business memories: {len(business_memories)} found")
    
    # List by user
    founder_memories = memory.list(user_id="founder_001")
    print(f"Founder memories: {len(founder_memories)} found")
    
    # Get specific memory by custom ID
    q2_data = memory.get("q2_target")
    print(f"Q2 Target: {q2_data}\n")
    
    # Semantic search still works
    print("4. Semantic search alongside direct access...")
    semantic_results = memory.recall(
        "financial performance",
        strategy=RecallStrategy.SEMANTIC,
        user_id="founder_001"
    )
    print(f"Semantic search for 'financial performance': {semantic_results}\n")
    
    # Memory management
    print("5. Memory lifecycle management...")
    
    # Update confidence
    if memory_ids:
        success = memory.update_confidence(memory_ids[0], 0.95)
        print(f"- Updated confidence: {success}")
    
    # GDPR compliance
    print("\n6. GDPR compliance features...")
    user_data = memory.export_user_data("founder_001")
    print(f"- Exported {user_data['memory_count']} memories for user")
    
    # Clean up old data
    deleted = memory.forget_before("2023-01-01", user_id="old_user")
    print(f"- Cleaned up {deleted} old memories\n")


def demo_use_cases():
    """Show real-world use cases"""
    print("=== Real-World Use Cases ===\n")
    
    # Customer support bot
    print("1. Customer Support Bot")
    support_memory = Memory(api_key="am_demo_key_xxx")
    support_memory.remember("Customer reported login issues", metadata={
        "ticket_id": "SUP-123",
        "category": "bug",
        "user_id": "customer_456"
    })
    
    # When customer returns
    context = support_memory.recall("previous issues", user_id="customer_456")
    print(f"Support context: {context}\n")
    
    # Personal AI agent
    print("2. Personal AI Agent")
    agent_memory = Memory(api_key="am_demo_key_xxx")
    agent_memory.remember("Prefers meetings in the morning")
    agent_memory.remember("Allergic to peanuts")
    agent_memory.remember("Birthday: June 15th")
    
    # Planning lunch
    lunch_context = agent_memory.recall("dietary restrictions")
    print(f"Lunch planning context: {lunch_context}\n")
    
    # Code agent
    print("3. Code Agent")
    code_memory = Memory(api_key="am_demo_key_xxx")
    code_memory.remember("Project uses TypeScript with strict mode")
    code_memory.remember("Prefers functional programming style")
    code_memory.remember("Testing with Jest and React Testing Library")
    
    # When writing new code
    code_context = code_memory.recall("coding preferences and project setup")
    print(f"Coding context: {code_context}\n")


if __name__ == "__main__":
    # Run all demos
    demo_basic_usage()
    print("\n" + "="*50 + "\n")
    demo_advanced_features()
    print("\n" + "="*50 + "\n")
    demo_use_cases()
    
    print("🚀 Ready to give your AI agents perfect memory?")
    print("Get started at https://agentmind.ai")