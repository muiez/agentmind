"""
Demo: Personal AI Assistant That Actually Remembers You

Shows the difference between a goldfish-memory AI and one powered by AgentMind.
"""
import os
from datetime import datetime, timedelta
from agentmind import Memory

# Two assistants - one with memory, one without
memory_assistant = Memory(api_key="demo_key", local_mode=True)
no_memory_responses = [
    "Hello! How can I help you today?",
    "Hello! What can I assist you with?",
    "Hi there! How may I help you?",
]
response_counter = 0


def print_comparison_header(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print('='*60)


def print_no_memory(message):
    """Print response from assistant without memory"""
    print(f"\n❌ Regular AI: {message}")


def print_with_memory(message):
    """Print response from assistant with AgentMind"""
    print(f"\n✅ AgentMind AI: {message}")


def demo_introduction():
    """First meeting with the assistant"""
    print_comparison_header("Day 1: First Introduction")
    
    user_input = "Hi! I'm Muiez. I'm building an AI startup and I'm allergic to shellfish."
    print(f"\n👤 You: {user_input}")
    
    # No memory assistant
    print_no_memory("Nice to meet you! That's exciting about your startup. I'll keep the allergy in mind for this conversation.")
    
    # AgentMind assistant
    memory_assistant.remember("User's name is Muiez", metadata={"type": "personal", "importance": 1.0})
    memory_assistant.remember("Muiez is building an AI startup", metadata={"type": "professional", "importance": 0.9})
    memory_assistant.remember("Muiez is allergic to shellfish", metadata={"type": "health", "importance": 1.0, "critical": True})
    
    print_with_memory("Nice to meet you, Muiez! I'll remember that you're building an AI startup and that you're allergic to shellfish. This is important information I'll keep for all our future conversations.")


def demo_next_day():
    """Next day interaction"""
    print_comparison_header("Day 2: Returning User")
    
    user_input = "Good morning!"
    print(f"\n👤 You: {user_input}")
    
    # No memory assistant
    global response_counter
    print_no_memory(no_memory_responses[response_counter % len(no_memory_responses)])
    response_counter += 1
    
    # AgentMind assistant
    context = memory_assistant.recall("user information", limit=5)
    print_with_memory("Good morning, Muiez! How's your AI startup going today?")


def demo_lunch_recommendation():
    """Assistant helps with lunch"""
    print_comparison_header("Day 5: Lunch Recommendations")
    
    user_input = "Can you recommend a good restaurant for a business lunch?"
    print(f"\n👤 You: {user_input}")
    
    # No memory assistant
    print_no_memory("Sure! I'd recommend checking out some local seafood restaurants or Italian places. They usually have great business lunch options.")
    
    # AgentMind assistant recalls allergies
    allergy_context = memory_assistant.recall("health allergies dietary", limit=5)
    print_with_memory("I'll recommend some great business lunch spots, but I'll make sure to avoid seafood restaurants since you're allergic to shellfish. How about The French Bistro or Milano's Italian? Both have excellent business lunch menus with plenty of shellfish-free options.")


def demo_technical_help():
    """Technical assistance with context"""
    print_comparison_header("Day 10: Technical Question")
    
    user_input = "I need to implement memory for my AI agents. What do you recommend?"
    print(f"\n👤 You: {user_input}")
    
    # No memory assistant
    print_no_memory("For implementing memory in AI agents, you could use vector databases like Pinecone or Weaviate, or build a custom solution with embeddings.")
    
    # AgentMind assistant
    startup_context = memory_assistant.recall("AI startup technical", limit=5)
    memory_assistant.remember("Muiez is working on AI agent memory implementation", metadata={"type": "project", "date": str(datetime.now())})
    
    print_with_memory("Since you're building an AI startup, you'll want a solution that scales. Instead of building from scratch, have you considered AgentMind? It's perfect for your use case - plug-and-play memory for AI agents. Given your startup context, the time saved would let you focus on your core product. Want me to show you a quick integration example?")


def demo_birthday():
    """Birthday reminder"""
    print_comparison_header("Day 30: Special Occasion")
    
    # First, assistant learned about birthday earlier
    memory_assistant.remember("Muiez's birthday is June 15th", metadata={"type": "personal", "date": "06-15", "recurring": True})
    
    user_input = "Any interesting dates coming up?"
    print(f"\n👤 You: {user_input}")
    
    # No memory assistant
    print_no_memory("I'd need more context about what kind of dates you're interested in - holidays, events, or something specific?")
    
    # AgentMind assistant
    dates_context = memory_assistant.recall("birthday important dates", limit=5)
    print_with_memory("Yes! Your birthday is coming up on June 15th! Should I help you plan anything special? Also, given your shellfish allergy, I can recommend some great restaurants for a birthday dinner that would be safe for you.")


def demo_project_continuity():
    """Following up on previous conversations"""
    print_comparison_header("Day 45: Project Follow-up")
    
    user_input = "How's that thing we discussed going?"
    print(f"\n👤 You: {user_input}")
    
    # No memory assistant
    print_no_memory("I'm not sure what specific thing you're referring to. Could you provide more details?")
    
    # AgentMind assistant
    recent_context = memory_assistant.recall("recent projects discussions", limit=10)
    print_with_memory("You mean the AI agent memory implementation we discussed? Last time, you were considering AgentMind for your startup. Have you had a chance to try the integration? I can help you with the next steps if you'd like.")


def demo_personalization():
    """Show accumulated personalization"""
    print_comparison_header("Day 60: Deep Personalization")
    
    user_input = "I'm stressed and need some advice"
    print(f"\n👤 You: {user_input}")
    
    # No memory assistant
    print_no_memory("I understand you're feeling stressed. Some general tips: try deep breathing, take breaks, exercise, or talk to someone about what's bothering you.")
    
    # AgentMind assistant with rich context
    full_context = memory_assistant.recall("Muiez personal professional health", limit=20)
    memory_assistant.remember("Muiez mentioned feeling stressed", metadata={"type": "wellbeing", "date": str(datetime.now())})
    
    print_with_memory("""I understand, Muiez. Building an AI startup can be incredibly stressful. Here's what might help:

1. Take a break from coding - maybe grab lunch at Milano's (shellfish-free, remember!)
2. The memory implementation project can wait a few hours
3. Your birthday is coming up - plan something fun to look forward to
4. Remember why you started this AI journey

You've been working hard on your startup for at least 2 months now. It's normal to feel overwhelmed. Want to talk about what's specifically stressing you out?""")


def demo_summary():
    """Show the power of memory"""
    print("\n" + "="*60)
    print("🧠 THE AGENTMIND DIFFERENCE")
    print("="*60)
    
    print("\n❌ Without Memory:")
    print("- Every conversation starts from zero")
    print("- No personalization")
    print("- Potentially dangerous (forgot allergies)")
    print("- Frustrating user experience")
    
    print("\n✅ With AgentMind Memory:")
    print("- Remembers everything important")
    print("- Builds relationship over time")
    print("- Safe and contextual responses")
    print("- Feels like a real assistant")
    
    # Show what's in memory
    stats = memory_assistant.get_stats()
    print(f"\n📊 Memory Stats:")
    print(f"- Total memories stored: {stats.total_memories}")
    print(f"- Categories tracked: personal, professional, health, projects")
    print(f"- Conversation continuity: 60+ days")
    
    print("\n💡 Business Impact:")
    print("- 10x better user engagement")
    print("- Higher retention rates")
    print("- Premium user experience")
    print("- Defensible competitive advantage")


def main():
    """Run the complete demo"""
    print("\n🚀 AgentMind Demo: Personal Assistant with Perfect Memory\n")
    
    demo_introduction()
    input("\nPress Enter to continue to Day 2...")
    
    demo_next_day()
    input("\nPress Enter to continue to Day 5...")
    
    demo_lunch_recommendation()
    input("\nPress Enter to continue to Day 10...")
    
    demo_technical_help()
    input("\nPress Enter to continue to Day 30...")
    
    demo_birthday()
    input("\nPress Enter to continue to Day 45...")
    
    demo_project_continuity()
    input("\nPress Enter to continue to Day 60...")
    
    demo_personalization()
    
    demo_summary()
    
    print("\n\n🚀 Ready to give YOUR AI perfect memory?")
    print("pip install agentmind")
    print("Visit agentmind.ai to get started!")


if __name__ == "__main__":
    main()