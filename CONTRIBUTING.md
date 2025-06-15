# Contributing to AgentMind

Thank you for your interest in contributing to AgentMind! We're building the memory layer for AI agents, and we'd love your help.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/agentmind.git
   cd agentmind
   ```
3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run tests:
   ```bash
   pytest
   ```

## 🛠️ Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8 agentmind/
black agentmind/ --check
```

## 📝 How to Contribute

### Reporting Bugs
- Check existing issues first
- Include Python version and OS
- Provide minimal reproduction code
- Describe expected vs actual behavior

### Suggesting Features
- Open an issue with [Feature Request] tag
- Explain the use case
- Provide examples if possible

### Submitting Code

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests for new features
   - Update documentation

3. **Test your changes**
   ```bash
   pytest
   black agentmind/
   ```

4. **Submit a Pull Request**
   - Clear description of changes
   - Reference any related issues
   - Ensure all tests pass

## 🎯 Areas We Need Help

- **Integrations**: LangChain, AutoGen, CrewAI, etc.
- **Storage Backends**: Redis, DynamoDB, etc.
- **Language SDKs**: JavaScript, Go, Rust
- **Documentation**: Tutorials, examples, guides
- **Performance**: Optimizations, benchmarks

## 💡 Design Principles

1. **Simplicity First**: APIs should be intuitive
2. **Performance Matters**: Keep recall <200ms
3. **Developer Experience**: If it's not easy, it's not done
4. **Extensibility**: Easy to add new features

## 🧪 Testing

- Write tests for all new features
- Maintain >80% code coverage
- Test files go in `tests/`
- Use pytest fixtures for common setups

Example test:
```python
def test_memory_recall():
    memory = Memory(api_key="test", local_mode=True)
    memory.remember("Test fact")
    results = memory.recall("test")
    assert "Test fact" in results
```

## 📖 Documentation

- Update docstrings for all public methods
- Add examples to the README for new features
- Create examples in `examples/` for complex features

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- No harassment or discrimination

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🎉 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

## Questions?

- Discord: [Join our community](https://discord.gg/agentmind)
- Email: contribute@agentmind.ai
- Twitter: [@agentmindai](https://twitter.com/agentmindai)

Thank you for making AgentMind better! 🧠✨