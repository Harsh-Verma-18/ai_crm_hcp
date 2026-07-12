from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
 
 
class AgentState(TypedDict):
    # `add_messages` reducer appends new messages instead of overwriting the
    # list, which is what lets the chatbot <-> tools loop keep full context.
    messages: Annotated[list[BaseMessage], add_messages]
 