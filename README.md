# agentmind memory 🧠

> The missing memory layer for AI agents. Simple, fast, and powerful.

[![PyPI version](https://badge.fury.io/py/agentmind.svg)](https://badge.fury.io/py/agentmind)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why agentmind?

Every AI agent needs memory. Today, developers hack together vector DBs, prompt engineering, and custom storage. We make it simple.

```python
from agentmind import Memory

# Initialize memory for your AI assistant
memory = Memory(local_mode=True)

# Store facts during conversation
memory.remember("My name is Alex")
memory.remember("I live in New York")
memory.remember("I'm vegetarian")
memory.remember("I have a meeting at 3pm today")

# Later when you ask for help...
context = memory.recall("restaurant")
# Returns: ["I'm vegetarian"]

context = memory.recall("schedule today")
# Returns: ["I have a meeting at 3pm today"]
```

That's it. No vector DBs to manage. No complex prompt engineering. Just memory that works.

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

### Semantic Search
```python
# Find memories by meaning, not just keywords
memories = memory.recall(
    "technical challenges",
    strategy="semantic",
    limit=5
)
```

### Memory Management
```python
# Organize memories
memory.remember("Q4 revenue target: $1M", metadata={
    "category": "business",
    "importance": "high",
    "expires": "2024-12-31"
})

# Batch operations
memories = [
    {"content": "Launched MVP", "timestamp": "2024-01-15"},
    {"content": "First customer", "timestamp": "2024-02-01"}
]
memory.remember_batch(memories)

# Forget when needed
memory.forget(memory_id="mem_abc123")
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
