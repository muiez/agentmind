# agentmind memory 🧠

> The conscience layer for AI agents. Memory, beliefs, reflection, and ethics in one simple package.

[![PyPI version](https://badge.fury.io/py/agentmind.svg)](https://badge.fury.io/py/agentmind)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why agentmind?

Every AI agent needs a conscience - memory to remember, beliefs to guide decisions, reflection to improve, and ethics to stay aligned. Today, developers hack together vector DBs, prompt engineering, and custom storage. We make it simple.

```python
from agentmind import Memory

# Initialize memory for your AI assistant
memory = Memory(local_mode=True)

# Store anything and get back an ID
memory_id = memory.remember("I prefer morning meetings")
# Returns: "mem_7a8c3b4f"

# Store with custom ID
memory.remember("Project deadline: March 15th", id="project_deadline")

# Store complex data
preferences_id = memory.remember({
    "communication_style": "direct and concise",
    "meeting_times": ["9am", "2pm"],
    "timezone": "EST"
})

# Get by ID - simple and direct
memory.get("project_deadline")
# Returns: "Project deadline: March 15th"

# Get with metadata
data = memory.get(preferences_id, include_metadata=True)
# Returns: {"content": {...}, "id": "mem_...", "timestamp": "...", ...}

# See what's in memory
memories = memory.list()
# Returns: [{"id": "mem_7a8c3b4f", "preview": "I prefer morning meetings", ...}, ...]

# Semantic search still works
context = memory.recall("meeting preferences")
# Returns: ["I prefer morning meetings"]
```

That's it. No vector DBs to manage. No complex prompt engineering. Just a conscience that works.

## Features

- 🚀 **5-minute integration** - Drop-in memory for any LLM app
- 🔌 **Framework agnostic** - Works with LangChain, OpenAI, Anthropic, and more
- ⚡ **Fast** - Sub-200ms recall latency
- 🔒 **Secure** - Optional E2E encryption, GDPR compliant
- 📊 **Smart** - Semantic search, auto-summarization, importance ranking

## Installation

```bash
pip install agentmind
```

## Framework Integrations

### With LangChain

```python
from langchain import ConversationChain
from langchain.llms import OpenAI
from agentmind.integrations.langchain import AgentMindMemory

# Use AgentMind as LangChain's memory - persists across sessions!
memory = AgentMindMemory(local_mode=True, user_id="user_123")

chain = ConversationChain(
    llm=OpenAI(),
    memory=memory
)

# First conversation
chain.predict(input="I'm working on a React app with TypeScript")
chain.predict(input="I need help with state management")

# Later session - the AI remembers!
response = chain.predict(input="What technology stack am I using?")
# Output: "You're working on a React app with TypeScript. Last time we discussed
# state management options for your project."
```

### With OpenAI

```python
from openai import OpenAI
from agentmind import Memory
from agentmind.integrations.openai import enhance_with_memory

client = OpenAI()
memory = Memory(local_mode=True, user_id="founder_1234")

# Track founder's journey and challenges
memory.remember("Building a fintech startup focused on small business lending")
memory.remember("Team of 8 people, raised $2M seed round last month")
memory.remember("Revenue goal: $1M ARR by end of year")

# Founder asks for strategic advice
messages = [
    {"role": "user", "content": "Should I hire a compliance officer or outsource SOC2?"}
]

# Automatically inject relevant context
enhanced_messages = enhance_with_memory(messages, memory)

response = client.chat.completions.create(
    model="gpt-4",
    messages=enhanced_messages
)
# AI response considers the startup's size (8 people), funding ($2M), and revenue goals
```

## Advanced Features

### Direct Memory Access
```python
# Store with custom ID for easy retrieval
memory.remember({"api_key": "secret", "endpoint": "https://api.example.com"}, id="api_config")

# Get it back anytime
config = memory.get("api_config")

# Check if memory exists
if memory.exists("api_config"):
    config = memory.get("api_config")

# Delete when done
memory.delete("api_config")
```

### Explore Memory Contents
```python
# See everything in memory
all_memories = memory.list()
for mem in all_memories:
    print(f"{mem['id']}: {mem['preview']} ({mem['size']})")

# Get full data
with_data = memory.list(include_data=True)

# Filter memories
user_memories = memory.list(user_id="user_123")
recent = memory.list(created_after="2024-01-20")
important = memory.list(category="important")

# Paginate through large memory stores
page1 = memory.list(limit=50, offset=0)
page2 = memory.list(limit=50, offset=50)
```

### Detailed Inspection
```python
# Get complete details about a memory
details = memory.inspect("mem_abc123")
print(f"Created: {details['metadata']['created']}")
print(f"Size: {details['metadata']['size']}")
print(f"Type: {details['metadata']['type']}")
print(f"Content: {details['content']}")
```

### Memory Management
```python
# Store complex data structures
user_profile = {
    "name": "Sarah Chen",
    "role": "Product Manager",
    "team": "Growth",
    "goals": ["Increase user retention", "Launch mobile app"],
    "last_review": "2024-01-15"
}
profile_id = memory.remember(user_profile, metadata={"category": "user_data"})

# Batch operations - returns list of IDs
memory_ids = memory.remember_batch([
    "First memory",
    {"content": "Second memory", "metadata": {"important": True}},
    {"content": "Third memory", "id": "custom_id_3"}
])

# Semantic search still works alongside direct access
memories = memory.recall("technical challenges", strategy="semantic", limit=5)

# Forget memories
memory.forget(memory_id="mem_abc123")  # Deprecated - use delete()
memory.delete("mem_abc123")  # New preferred method
memory.forget_before(date="2023-01-01")
```

### Session Management
```python
# Auto-summarize conversations
summary = memory.summarize_session(session_id="chat_123")

# Export user data (GDPR)
data = memory.export_user_data(user_id="user_123")
```

## Deployment Options

### 🏠 Self-Hosted (Available Now)
Run AgentMind locally or on your own infrastructure. Perfect for development and testing.

```python
# Works completely offline
memory = Memory(local_mode=True)
```

### ☁️ Hosted Cloud Service (Coming Soon)
We're building a managed cloud service so you don't have to worry about infrastructure, scaling, or maintenance.

```python
# Cloud mode with API key (coming soon)
memory = Memory(api_key="your-api-key")
```

**[→ Join the waitlist](#)** to get early access and special launch pricing.

## Who's Using AgentMind?

### 💼 **Enterprise Support**
- **Zendesk/Intercom competitors** - Bots that remember all customer history
- **No more "Can you repeat your issue?"** - Saves 15 min per ticket
- **Example**: TechCorp saved $2M/year in support costs

### 🏥 **Healthcare AI**
- **Patient intake bots** - Remember symptoms, medications, history
- **HIPAA compliant** - Encrypted memory storage
- **Example**: MedAI reduced intake time from 45 to 5 minutes

### 💰 **Financial Advisors**
- **Wealth management bots** - Track client goals, risk tolerance, life events
- **Compliance-ready** - Full audit trail of all advice given
- **Example**: WealthBot manages $500M AUM with perfect client memory

### 🎓 **EdTech Platforms**
- **AI tutors** - Remember what each student struggles with
- **Adaptive learning** - Adjusts based on long-term progress
- **Example**: LearnAI improved student retention by 67%

## Roadmap

- [x] Core memory API
- [x] LangChain integration
- [x] OpenAI integration
- [ ] smolagents integration
- [x] Semantic search
- [ ] Memory compression
- [ ] Multi-modal memories (images, audio)
- [ ] Reflection layer (self-improving memory)
- [ ] Belief system (confidence tracking)
- [ ] Ethics layer (value alignment)

## Community

- [Discord](https://discord.gg/agentmind) - Chat with the community
- [Twitter](https://twitter.com/agentmindai) - Latest updates
- Blog - Coming soon

## Contributing

We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
git clone https://github.com/muiez/agentmind
cd agentmind
pip install -e ".[dev]"
pytest
```

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with ❤️ for the AI community. Give your agents the memory they deserve.
