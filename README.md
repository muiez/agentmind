# agentmind memory 🧠

> The missing memory layer for AI agents. Simple, fast, and powerful.

[![PyPI version](https://badge.fury.io/py/agentmind.svg)](https://badge.fury.io/py/agentmind)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why agentmind?

Every AI agent needs memory. Today, developers hack together vector DBs, prompt engineering, and custom storage. We make it simple.

```python
from agentmind import Memory

# Initialize once
memory = Memory(local_mode=True)  # No API key needed

# Remember anything
memory.remember("User prefers Python over JavaScript")

# Recall when needed
context = memory.recall("What programming languages does the user like?")
# Returns: ["User prefers Python over JavaScript"]
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

## Quick Start

### Basic Usage

```python
from agentmind import Memory

memory = Memory(local_mode=True)

# Store memories
memory.remember("User is building a startup in AI")
memory.remember("Prefers concise responses", metadata={"importance": "high"})

# Recall relevant context
context = memory.recall("What do I know about the user?")
print(context)
# > ["User is building a startup in AI", "Prefers concise responses"]
```

### With LangChain

```python
from langchain import ConversationChain
from agentmind.integrations.langchain import agentmindMemory

memory = AgentMindMemory(local_mode=True, user_id="user123")

chain = ConversationChain(
    llm=your_llm,
    memory=memory
)

response = chain.predict(input="Hi, I'm working on my AI startup today")
# Memory automatically stores the conversation
```

### With OpenAI

```python
from openai import OpenAI
from agentmind.integrations.openai import enhance_with_memory

client = OpenAI()
memory = Memory(local_mode=True)

# Enhance your chat with memory
messages = [
    {"role": "user", "content": "What did we discuss about my startup?"}
]

# AgentMind automatically adds relevant context
enhanced_messages = enhance_with_memory(messages, memory)

response = client.chat.completions.create(
    model="gpt-4",
    messages=enhanced_messages
)
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

## Use Cases

- 🤖 **Chatbots** - Give your bot long-term memory across conversations
- 🎯 **Personal Assistants** - Remember user preferences and history
- 💼 **Sales Agents** - Track customer interactions and insights
- 🏥 **Healthcare Bots** - Maintain patient context (HIPAA compliant)
- 📚 **Education** - Personalized tutoring with memory of progress

## Roadmap

- [x] Core memory API
- [x] LangChain integration
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
