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
    
    # Store some memories
    print("1. Storing memories...")
    memory.remember("User prefers Python for backend development", metadata={"category": "tech_preference"})
    memory.remember("User mentioned they have expertise in ML compilers", metadata={"importance": 0.9})
    memory.remember("Meeting scheduled for next Tuesday at 3pm", metadata={"category": "calendar"})
    print("✓ Stored 3 memories\n")
    
    # Recall memories
    print("2. Recalling relevant context...")
    context = memory.recall("What programming language does the user prefer?")
    print(f"Query: 'What programming language does the user prefer?'")
    print(f"Results: {context}\n")
    
    # Get facts by category
    print("3. Getting categorized facts...")
    tech_facts = memory.get_facts(category="tech_preference")
    print(f"Tech preferences: {[f['content'] for f in tech_facts]}\n")
    
    # Get recent memories
    print("4. Getting recent memories (last 24 hours)...")
    recent = memory.get_recent(hours=24)
    print(f"Recent: {recent[:2]}...\n")  # Show first 2
    
    # Demonstrate session management
    print("5. Session management...")
    session_id = "demo_session_001"
    memory.remember("Discussed memory layer architecture", session_id=session_id)
    memory.remember("Target: 200ms recall latency", session_id=session_id)
    
    summary = memory.summarize_session(session_id)
    print(f"Session summary: {summary}\n")
    
    # Show statistics
    print("6. Memory statistics...")
    stats = memory.get_stats()
    print(f"Total memories: {stats.total_memories}")
    print(f"Total users: {stats.total_users}")
    print(f"Popular categories: {stats.popular_categories}\n")


def demo_advanced_features():
    """Demonstrate advanced memory features"""
    print("=== Advanced Features ===\n")
    
    # Batch operations
    print("1. Batch memory storage...")
    memories = [
        {"content": "Q1 revenue: $50k", "metadata": {"category": "business", "importance": 0.8}},
        {"content": "Q2 target: $150k", "metadata": {"category": "business", "importance": 0.9}},
        {"content": "Hired first engineer", "metadata": {"category": "team", "importance": 0.9}}
    ]
    memory.remember_batch(memories, user_id="founder_001")
    print("✓ Stored batch of 3 memories\n")
    
    # Different recall strategies
    print("2. Testing recall strategies...")
    
    # Semantic search
    semantic_results = memory.recall(
        "financial performance",
        strategy=RecallStrategy.SEMANTIC,
        user_id="founder_001"
    )
    print(f"Semantic search for 'financial performance': {semantic_results}\n")
    
    # Memory management
    print("3. Memory lifecycle management...")
    
    # Update confidence
    # In a real scenario, you'd have the memory_id from remember()
    print("- Updating memory confidence scores")
    
    # GDPR compliance
    print("4. GDPR compliance features...")
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
    
    # Personal assistant
    print("2. Personal Assistant")
    assistant_memory = Memory(api_key="am_demo_key_xxx")
    assistant_memory.remember("Prefers meetings in the morning")
    assistant_memory.remember("Allergic to peanuts")
    assistant_memory.remember("Birthday: June 15th")
    
    # Planning lunch
    lunch_context = assistant_memory.recall("dietary restrictions")
    print(f"Lunch planning context: {lunch_context}\n")
    
    # Code assistant
    print("3. Code Assistant")
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