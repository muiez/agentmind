# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AgentMind is a Python package that provides a "conscience layer" for AI agents - think of it as long-term memory for your AI applications. Currently in alpha (v0.1.5), it supports local-mode only with cloud service planned.

## Development Setup

1. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Run tests:
   ```bash
   pytest                    # Run all tests
   pytest tests/test_memory.py::TestMemoryCore::test_remember  # Run specific test
   pytest -v                 # Verbose output
   pytest -k "test_recall"   # Run tests matching pattern
   ```

3. Code formatting and linting:
   ```bash
   black agentmind tests     # Format code
   flake8 agentmind tests    # Lint code
   ```

## Architecture

### Core Components

1. **agentmind/memory.py** - Main Memory class with core functionality:
   - `remember()` - Store memories with automatic tagging
   - `recall()` - Retrieve memories using various strategies
   - Session management and summarization
   - GDPR compliance methods

2. **agentmind/types.py** - Pydantic models for type safety:
   - `MemoryInput`, `MemoryOutput`, `RecallOptions`
   - Validation and serialization logic

3. **agentmind/integrations/** - Framework adapters:
   - `langchain.py` - LangChain chat memory integration
   - `openai.py` - OpenAI conversation history adapter

### Memory Storage

- Currently uses ChromaDB for local vector storage
- Memories stored with embeddings for semantic search
- Session-based organization with automatic summarization
- Batch operations supported for efficiency

### Key Design Patterns

1. **Flexible Recall Strategies**:
   - `semantic` - Vector similarity search
   - `recency` - Time-based retrieval
   - `importance` - Score-based filtering
   - `hybrid` - Combined approach

2. **Session Management**:
   - Automatic session creation if not specified
   - Session summaries for context preservation
   - Cross-session search capabilities

3. **Type Safety**:
   - Pydantic models for all inputs/outputs
   - Runtime validation and helpful error messages

## Common Development Tasks

### Adding New Features
1. Implement in appropriate module (likely `memory.py`)
2. Add type definitions to `types.py` if needed
3. Write tests in `tests/test_memory.py`
4. Update examples if adding user-facing functionality

### Testing Patterns
- Tests use `TestMemoryCore` base class for common setup
- Each test method should test one specific behavior
- Use descriptive test names: `test_<method>_<scenario>`
- Mock external dependencies when possible

### Code Standards
- Follow existing patterns in the codebase
- Use type hints for all function parameters and returns
- Docstrings for all public methods
- Keep methods focused and single-purpose

## Important Context

### Current Limitations
- Local mode only (no cloud sync yet)
- Single-user design
- No built-in authentication
- Limited to text memories

### Package Structure
```
agentmind/
├── __init__.py          # Package exports
├── memory.py            # Core Memory class
├── types.py             # Type definitions
├── integrations/        # Framework adapters
│   ├── langchain.py
│   └── openai.py
└── utils.py            # Helper functions
```

### Dependencies
- chromadb: Vector database
- pydantic: Data validation
- Optional: langchain, openai for integrations

## Quick Reference

### Basic Usage
```python
from agentmind import Memory

memory = Memory()
memory.remember("Important fact")
memories = memory.recall("What did I learn?")
```

### With LangChain
```python
from agentmind.integrations.langchain import AgentMindChatMemory

memory = AgentMindChatMemory(session_id="chat-session")
# Use with LangChain chains
```

### Running Examples
```bash
python examples/basic_usage.py
python examples/langchain_example.py
python examples/openai_example.py
```