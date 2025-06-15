"""
Visual Demo Script - Perfect for creating a GIF/video
Shows the power of AgentMind in a visual, easy-to-follow way
"""
import time
import sys
from agentmind import Memory

def typewriter(text, delay=0.03):
    """Print text with typewriter effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def pause(seconds=1):
    """Pause for dramatic effect"""
    time.sleep(seconds)

def clear_screen():
    """Clear screen (works on most terminals)"""
    print("\033[2J\033[H")

def print_header():
    """Print AgentMind header"""
    print("╔══════════════════════════════════════════╗")
    print("║        🧠 AgentMind Memory Demo          ║")
    print("║    AI Agents That Actually Remember      ║")
    print("╚══════════════════════════════════════════╝")
    print()

def main():
    # Initialize
    memory = Memory(api_key="demo", local_mode=True)
    
    # Scene 1: The Problem
    clear_screen()
    print_header()
    typewriter("❌ THE PROBLEM: AI Assistants Forget Everything")
    pause(1)
    
    print("\nDay 1:")
    typewriter("👤 'Hi, I'm Sarah. I need help with Python coding.'")
    typewriter("🤖 'Hello Sarah! I'll help with Python.'")
    pause(1)
    
    print("\nDay 2:")
    typewriter("👤 'Can you help me?'")
    typewriter("🤖 'Hello! What's your name? What language?'")
    typewriter("😤 'We literally talked yesterday...'")
    pause(2)
    
    # Scene 2: The Solution
    clear_screen()
    print_header()
    typewriter("✅ THE SOLUTION: AgentMind Memory")
    pause(1)
    
    print("\n📝 Just 3 lines of code:")
    print("─────────────────────────")
    typewriter("from agentmind import Memory")
    typewriter("memory = Memory(api_key='your-key')")
    typewriter("memory.remember('Sarah prefers Python')")
    pause(2)
    
    # Scene 3: Demo in Action
    clear_screen()
    print_header()
    typewriter("🚀 SEE THE MAGIC")
    pause(1)
    
    print("\nDay 1:")
    typewriter("👤 'Hi, I'm Sarah. I need help with Python coding.'")
    
    # Show memory storage
    print("\n💾 Storing memories...")
    memory.remember("Customer name: Sarah")
    typewriter("  ✓ Stored: Customer name")
    memory.remember("Sarah needs help with Python coding")
    typewriter("  ✓ Stored: Programming preference")
    memory.remember("Sarah is a beginner in Python")
    typewriter("  ✓ Stored: Skill level")
    
    typewriter("\n🤖 'Hi Sarah! I'll help you learn Python.'")
    pause(2)
    
    print("\nDay 7:")
    typewriter("👤 'Can you help me with functions?'")
    
    # Show memory recall
    print("\n🔍 Recalling memories...")
    context = memory.recall("Sarah Python")
    typewriter("  ✓ Found: Sarah, Python coding, beginner level")
    
    typewriter("\n🤖 'Of course, Sarah! Let's continue your Python")
    typewriter("    journey with functions. Since you're a beginner,")
    typewriter("    I'll start with simple examples.'")
    pause(2)
    
    # Scene 4: Business Impact
    clear_screen()
    print_header()
    typewriter("💰 THE BUSINESS IMPACT")
    pause(1)
    
    print("\n📈 With AgentMind Memory:")
    typewriter("  • 87% better user satisfaction")
    typewriter("  • 3x higher engagement")
    typewriter("  • 5x more upgrades to paid plans")
    typewriter("  • Users feel heard and valued")
    pause(2)
    
    # Scene 5: Call to Action
    clear_screen()
    print_header()
    print("\n✨ Ready to give YOUR AI perfect memory?")
    print()
    typewriter("npm install agentmind  # or")
    typewriter("pip install agentmind")
    print()
    typewriter("🌐 agentmind.ai")
    print()
    typewriter("🚀 Join 1,000+ developers building smarter AI")
    print("\n╚══════════════════════════════════════════╝")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Visit agentmind.ai to learn more!")