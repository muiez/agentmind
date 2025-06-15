"""
LangChain integration for AgentMind Memory
"""
from typing import List, Dict, Any, Optional
from langchain.schema import BaseMemory
from langchain.memory.chat_memory import BaseChatMemory
from langchain.schema.messages import BaseMessage, HumanMessage, AIMessage

from ..memory import Memory
from ..types import RecallStrategy


class AgentMindMemory(BaseChatMemory):
    """
    LangChain-compatible memory using AgentMind.
    
    Example:
        from langchain import ConversationChain
        from agentmind.integrations.langchain import AgentMindMemory
        
        memory = AgentMindMemory(api_key="am_live_xxx", user_id="user123")
        chain = ConversationChain(llm=llm, memory=memory)
    """
    
    memory: Memory
    user_id: str
    session_id: Optional[str] = None
    recall_limit: int = 5
    strategy: RecallStrategy = RecallStrategy.HYBRID
    memory_key: str = "history"
    input_key: Optional[str] = None
    output_key: Optional[str] = None
    
    def __init__(
        self,
        api_key: str,
        user_id: str,
        session_id: Optional[str] = None,
        recall_limit: int = 5,
        **kwargs
    ):
        """Initialize AgentMind memory for LangChain"""
        super().__init__(**kwargs)
        self.memory = Memory(api_key=api_key)
        self.user_id = user_id
        self.session_id = session_id
        self.recall_limit = recall_limit
        self.chat_memory = []  # Local buffer for current conversation
    
    @property
    def memory_variables(self) -> List[str]:
        """Return memory variables."""
        return [self.memory_key]
    
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Load relevant memories based on input."""
        # Get the input text
        input_text = inputs.get(self.input_key or list(inputs.keys())[0])
        
        # Recall relevant memories
        memories = self.memory.recall(
            query=input_text,
            strategy=self.strategy,
            limit=self.recall_limit,
            user_id=self.user_id
        )
        
        # Format memories for context
        context = []
        if memories:
            context.append("Relevant context from memory:")
            context.extend(f"- {mem}" for mem in memories)
        
        # Add recent chat history
        if self.chat_memory:
            context.append("\nRecent conversation:")
            for msg in self.chat_memory[-4:]:  # Last 4 messages
                if isinstance(msg, HumanMessage):
                    context.append(f"Human: {msg.content}")
                elif isinstance(msg, AIMessage):
                    context.append(f"AI: {msg.content}")
        
        return {self.memory_key: "\n".join(context)}
    
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context to memory."""
        # Get input and output
        input_text = inputs.get(self.input_key or list(inputs.keys())[0])
        output_text = outputs.get(self.output_key or list(outputs.keys())[0])
        
        # Store in AgentMind
        self.memory.remember(
            f"User said: {input_text}",
            metadata={"type": "user_message"},
            user_id=self.user_id,
            session_id=self.session_id
        )
        
        self.memory.remember(
            f"AI responded: {output_text}",
            metadata={"type": "ai_response"},
            user_id=self.user_id,
            session_id=self.session_id
        )
        
        # Update local chat buffer
        self.chat_memory.extend([
            HumanMessage(content=input_text),
            AIMessage(content=output_text)
        ])
        
        # Keep buffer size reasonable
        if len(self.chat_memory) > 10:
            self.chat_memory = self.chat_memory[-10:]
    
    def clear(self) -> None:
        """Clear session memories."""
        if self.session_id:
            self.memory.clear_session(self.session_id)
        self.chat_memory = []
    
    def summarize(self) -> str:
        """Summarize the current session."""
        if self.session_id:
            return self.memory.summarize_session(self.session_id)
        return "No session to summarize"