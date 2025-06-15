# AgentMind Memory 🧠

> The missing memory layer for AI agents. Simple, fast, and powerful.

[![PyPI](https://img.shields.io/pypi/v/agentmind-memory)](https://pypi.org/project/agentmind-memory/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/discord/123456789)](https://discord.gg/agentmind)

## Why AgentMind?

Every AI agent needs memory. Today, developers hack together vector DBs, prompt engineering, and custom storage. We make it simple.

```python
from agentmind import Memory

# Initialize once
memory = Memory(api_key="your-api-key")

# Remember anything
memory.remember("User prefers Python over JavaScript")

# Recall when needed
context = memory.recall("What programming languages does the user like?")
```

That's it. No vector DBs to manage. No complex prompt engineering. Just memory that works.

## Features

- 🚀 **5-minute integration** - Drop-in memory for any LLM app
- 🔌 **Framework agnostic** - Works with LangChain, OpenAI, Anthropic, and more
- ⚡ **Fast** - Sub-200ms recall latency (p99)
- 🔒 **Secure** - Optional E2E encryption, GDPR compliant
- 📊 **Smart** - Semantic search, auto-summarization, importance ranking

## Installation

```bash
pip install agentmind-memory
```

## Quick Start

### Basic Usage

```python
from agentmind import Memory

memory = Memory(api_key="am_live_xxx")

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
from agentmind.integrations.langchain import AgentMindMemory

memory = AgentMindMemory(api_key="am_live_xxx", user_id="user123")

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
memory = Memory(api_key="am_live_xxx")

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

## Pricing

| Plan | Memories | Recalls/mo | Price |
|------|----------|------------|-------|
| **Free** | 10,000 | 100,000 | $0 |
| **Pro** | 100,000 | 1M | $99/mo |
| **Business** | Unlimited | Unlimited | $499/mo |
| **Enterprise** | Custom | Custom | [Contact us](mailto:sales@agentmind.ai) |

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
- [Blog](https://agentmind.ai/blog) - Tutorials and insights

## Contributing

We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
git clone https://github.com/agentmind-ai/agentmind
cd agentmind
pip install -e ".[dev]"
pytest
```

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with ❤️ for the AI community. Give your agents the memory they deserve.