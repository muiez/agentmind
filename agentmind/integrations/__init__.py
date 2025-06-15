"""
Integrations for popular AI frameworks
"""

# Import integrations
try:
    from .openai import enhance_with_memory, create_memory_plugin, OpenAIMemoryWrapper
except ImportError:
    # OpenAI not installed
    pass

try:
    from .langchain import AgentMindMemory
except ImportError:
    # LangChain not installed
    pass