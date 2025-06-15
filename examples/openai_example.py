#!/usr/bin/env python
"""
Example: Using AgentMind with OpenAI
"""

from agentmind import Memory
from agentmind.integrations.openai import enhance_with_memory

# Note: You'll need to install openai and set your API key
# pip install openai
# export OPENAI_API_KEY='your-key'

def demo_without_openai_client():
    """Demo that works without OpenAI client"""
    print("🧠 AgentMind + OpenAI Integration Demo")
    print("=" * 50)
    
    # Initialize memory
    memory = Memory(local_mode=True)
    
    # Store some context
    print("\n📝 Storing memories...")
    memory.remember("User's name is Alice")
    memory.remember("User is learning machine learning")
    memory.remember("User prefers Python and PyTorch")
    memory.remember("User's goal is to build a recommendation system")
    
    # Simulate a conversation
    messages = [
        {"role": "user", "content": "Can you help me with my project?"}
    ]
    
    # Enhance with memory
    print("\n🔧 Enhancing messages with memory...")
    enhanced_messages = enhance_with_memory(messages, memory)
    
    print("\n📨 Enhanced messages for OpenAI:")
    for msg in enhanced_messages:
        print(f"\n[{msg['role'].upper()}]")
        print(msg['content'])
    
    print("\n✨ The AI now has context about Alice's ML project!")


def demo_with_openai_client():
    """Full demo with OpenAI client (requires API key)"""
    try:
        from openai import OpenAI
    except ImportError:
        print("⚠️  OpenAI not installed. Run: pip install openai")
        return
    
    print("\n\n🤖 Full OpenAI Integration Demo")
    print("=" * 50)
    
    # Initialize
    client = OpenAI()  # Uses OPENAI_API_KEY env var
    memory = Memory(local_mode=True)
    
    # Store context
    memory.remember("User is building a trading bot")
    memory.remember("User needs help with technical indicators")
    memory.remember("User prefers simple explanations")
    
    # Create conversation
    messages = [
        {"role": "user", "content": "What indicators should I use?"}
    ]
    
    # Enhance and call OpenAI
    enhanced_messages = enhance_with_memory(messages, memory)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=enhanced_messages,
            temperature=0.7
        )
        
        print("\n🤖 AI Response:")
        print(response.choices[0].message.content)
        
        # Store the response in memory too
        memory.remember(f"AI recommended: {response.choices[0].message.content[:100]}...")
        
    except Exception as e:
        print(f"⚠️  OpenAI API call failed: {e}")
        print("Make sure your OPENAI_API_KEY is set correctly")


if __name__ == "__main__":
    # Demo without requiring OpenAI API key
    demo_without_openai_client()
    
    # Uncomment to run with real OpenAI client
    # demo_with_openai_client()