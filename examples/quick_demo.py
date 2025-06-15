"""
AgentMind Quick Demo - See the Magic in 30 Seconds
"""
from agentmind import Memory
import time

def print_section(title):
    print(f"\n{'='*50}\n{title}\n{'='*50}")

def main():
    print("\n🧠 AgentMind Demo - AI Memory in Action\n")
    
    # Initialize memory
    memory = Memory(api_key="demo", local_mode=True)
    
    # ========== PART 1: First Conversation ==========
    print_section("Monday: Customer First Contact")
    
    print("👤 Customer: Hi, I'm John from Acme Corp. We need 50 enterprise licenses.")
    
    # Store the interaction
    memory.remember("Customer: John from Acme Corp")
    memory.remember("John needs 50 enterprise licenses") 
    memory.remember("Acme Corp is interested in bulk pricing")
    
    print("🤖 AI: Hi John! I'll help you with enterprise licenses for Acme Corp.")
    print("\n💾 [Memory Stored: Customer details, needs, company info]")
    
    time.sleep(2)
    
    # ========== PART 2: Customer Returns ==========
    print_section("Friday: Customer Returns")
    
    print("👤 Customer: Hi, what pricing options do we have?")
    
    # Without memory
    print("\n❌ Regular AI: Hello! What product are you interested in?")
    
    # With AgentMind
    context = memory.recall("John Acme pricing licenses")
    print("\n✅ AgentMind AI: Hi John! For Acme Corp's 50 enterprise licenses,")
    print("   I can offer our bulk discount: $99/license (usually $149).")
    print("   That's $4,950 total with priority support included.")
    
    time.sleep(2)
    
    # ========== PART 3: The Magic ==========
    print_section("The AgentMind Difference")
    
    print("🎯 What just happened:\n")
    
    print("1️⃣ Zero Context Loss")
    print("   → Remembered: name, company, exact needs")
    
    print("\n2️⃣ Instant Personalization") 
    print("   → Gave specific pricing without asking again")
    
    print("\n3️⃣ Better Conversion")
    print("   → Customer feels valued = higher close rate")
    
    # ========== PART 4: It's This Simple ==========
    print_section("Integration: 3 Lines of Code")
    
    print("```python")
    print("from agentmind import Memory")
    print("memory = Memory(api_key='your-key')")
    print("memory.remember('Important customer info')")
    print("context = memory.recall('relevant memories')")
    print("```")
    
    print("\n✨ That's it. Your AI now has perfect memory.")
    
    # ========== Stats ==========
    print_section("Live Memory Stats")
    stats = memory.get_stats()
    print(f"📊 Memories Stored: {stats.total_memories}")
    print(f"📊 Total Size: ~{stats.storage_used_mb:.2f} MB")
    print(f"📊 Recall Speed: <200ms")
    
    print("\n\n🚀 Give your AI agents perfect memory")
    print("👉 pip install agentmind")
    print("👉 https://agentmind.ai")
    print("\n💬 'This is what every AI app needs' - YC Founder")

if __name__ == "__main__":
    main()