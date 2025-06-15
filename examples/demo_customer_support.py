"""
Demo: Customer Support Bot with Perfect Memory

Shows how AgentMind transforms a basic chatbot into one that remembers
every customer interaction, preference, and issue.
"""
import os
import time
from datetime import datetime, timedelta
from agentmind import Memory

# Initialize memory (use local mode for demo)
memory = Memory(api_key="demo_key", local_mode=True)


def print_bot(message):
    """Print bot message with formatting"""
    print(f"\n🤖 Support Bot: {message}")


def print_user(message):
    """Print user message with formatting"""
    print(f"\n👤 Customer: {message}")


def print_memory_action(action, content):
    """Show what's happening with memory"""
    print(f"\n💾 [{action}] {content}")


def demo_first_interaction():
    """First customer interaction"""
    print("\n" + "="*60)
    print("DEMO: AI Support Bot with AgentMind Memory")
    print("="*60)
    
    print("\n--- Day 1: Customer's First Contact ---")
    
    # Customer introduces themselves
    print_user("Hi, I'm Sarah Chen. I just bought your Pro plan but I can't access the API dashboard.")
    
    # Bot remembers customer details
    memory.remember(
        "Customer: Sarah Chen",
        metadata={"type": "customer_info", "customer_id": "cust_789"}
    )
    print_memory_action("Storing", "Customer name: Sarah Chen")
    
    memory.remember(
        "Sarah Chen purchased Pro plan",
        metadata={"type": "purchase_info", "plan": "pro", "customer_id": "cust_789"}
    )
    print_memory_action("Storing", "Purchase info: Pro plan")
    
    memory.remember(
        "Sarah Chen reported issue: Cannot access API dashboard",
        metadata={"type": "issue", "status": "open", "customer_id": "cust_789"}
    )
    print_memory_action("Storing", "Issue: API dashboard access")
    
    print_bot("Hi Sarah! I see you've purchased our Pro plan. Let me help you with the API dashboard access. Can you try logging out and back in? Sometimes the permissions take a few minutes to sync.")
    
    print_user("Okay, trying now... Yes! That worked. Thanks!")
    
    # Update issue status
    memory.remember(
        "Sarah Chen's API dashboard issue resolved by re-login",
        metadata={"type": "resolution", "issue": "api_dashboard", "customer_id": "cust_789"}
    )
    print_memory_action("Storing", "Issue resolved: re-login fixed it")
    
    print_bot("Great! Is there anything else I can help you with?")
    
    print_user("Actually yes - I prefer email communications over chat. And I'm working on a Python project.")
    
    # Remember preferences
    memory.remember(
        "Sarah Chen prefers email communication",
        metadata={"type": "preference", "category": "communication", "customer_id": "cust_789"}
    )
    memory.remember(
        "Sarah Chen is working on a Python project",
        metadata={"type": "context", "category": "technical", "customer_id": "cust_789"}
    )
    print_memory_action("Storing", "Preferences: email, Python developer")
    
    print_bot("Noted! I'll make sure we follow up via email, and I'll keep in mind you're using Python. Have a great day!")


def demo_second_interaction():
    """Customer returns a week later"""
    print("\n\n--- Day 8: Customer Returns ---")
    
    print_user("Hi, I'm having another issue")
    
    # Bot recalls previous context
    print_memory_action("Recalling", "memories about this customer...")
    
    context = memory.recall("Sarah Chen customer history", limit=10)
    
    print_bot("Hi Sarah! Good to see you again. I remember you're on our Pro plan and you're working with Python. What issue are you experiencing today?")
    
    print_user("Wow, you remember me! Yes, I'm trying to use the batch API but getting rate limit errors.")
    
    # Bot uses previous context
    print_bot("Since you prefer email communication, I can send you a detailed guide on batch API optimization for Python. But quick tip: Pro plan has 1000 requests/minute. Are you using our Python SDK's built-in rate limiter?")
    
    memory.remember(
        "Sarah Chen experiencing rate limit errors with batch API",
        metadata={"type": "issue", "api": "batch", "customer_id": "cust_789"}
    )
    print_memory_action("Storing", "New issue: batch API rate limits")
    
    print_user("No, I didn't know about that! Can you show me?")
    
    print_bot("Of course! Here's a Python example:")
    print("\n```python")
    print("from agentmind import Memory, RateLimiter")
    print("memory = Memory(api_key='your-key', rate_limiter=RateLimiter(max_rpm=1000))")
    print("```")
    
    memory.remember(
        "Showed Sarah Chen rate limiter code for Python SDK",
        metadata={"type": "support_action", "topic": "rate_limiting", "customer_id": "cust_789"}
    )
    
    print_user("Perfect! This is why I love your support. You actually remember our conversations!")


def demo_third_interaction():
    """Customer returns after a month"""
    print("\n\n--- Day 30: Customer Needs Help Again ---")
    
    print_user("Hey, it's Sarah. I need help with something")
    
    # Recall full history
    history = memory.recall("Sarah Chen complete history", limit=20)
    
    print_bot("Hi Sarah! Welcome back. I see you've been with us for a month now on the Pro plan. You've previously had issues with API dashboard access (which we resolved) and rate limiting with the batch API. How can I help today?")
    
    print_user("I'm impressed you remember all that! I'm considering upgrading to Business plan. What's my usage been like?")
    
    # Bot can provide personalized recommendations
    memory.remember(
        "Sarah Chen considering upgrade to Business plan",
        metadata={"type": "sales_opportunity", "current_plan": "pro", "target_plan": "business", "customer_id": "cust_789"}
    )
    
    print_bot("Based on your history, you've been hitting rate limits with batch processing. The Business plan offers 10,000 requests/minute - 10x your current limit. Since you're doing Python batch processing, this would eliminate your bottlenecks.")
    
    print_bot("Also, I'll email you a personalized upgrade offer with a 20% discount for loyal customers like you. Check your inbox!")
    
    print_user("This is incredible. You know exactly what I need. Yes, please send that offer!")


def demo_analytics():
    """Show aggregated insights from memory"""
    print("\n\n--- Analytics Dashboard ---")
    print("\n📊 Customer Insights from AgentMind Memory:\n")
    
    # Get Sarah's profile
    sarah_facts = memory.get_facts(user_id="cust_789")
    
    print("Customer Profile:")
    print("- Name: Sarah Chen")
    print("- Plan: Pro (considering Business)")
    print("- Preferences: Email communication, Python developer")
    print("- Issues Resolved: 2 (API dashboard, rate limits)")
    print("- Satisfaction: High (repeat interactions)")
    print("- Upgrade Potential: Very High")
    
    print("\n💡 AI-Generated Insights:")
    print("- Customer is technically proficient (understood rate limiter quickly)")
    print("- Values personalized support (mentioned loving the memory feature)")
    print("- Ready for upsell (hitting plan limits, asking about upgrade)")


def main():
    """Run the full demo"""
    print("\n🚀 AgentMind Memory Demo - Starting...\n")
    time.sleep(1)
    
    # Run through customer journey
    demo_first_interaction()
    time.sleep(2)
    
    demo_second_interaction()
    time.sleep(2)
    
    demo_third_interaction()
    time.sleep(2)
    
    demo_analytics()
    
    print("\n\n" + "="*60)
    print("🎯 THE POWER OF AGENTMIND MEMORY")
    print("="*60)
    
    print("\n✅ Without AgentMind: Generic, repetitive support")
    print("✅ With AgentMind: Personalized, context-aware, memorable")
    
    print("\n💰 Business Impact:")
    print("- Higher customer satisfaction (CSAT)")
    print("- Increased upgrade rates")
    print("- Reduced support tickets")
    print("- Better customer retention")
    
    print("\n🔗 Get started in 5 minutes:")
    print("pip install agentmind")
    print("memory = Memory(api_key='your-key')")
    print("memory.remember('Customer insight')")
    print("\n🚀 Give your AI agents perfect memory at agentmind.ai")


if __name__ == "__main__":
    main()