from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
 
from app.ai_agent.state import AgentState
from app.ai_agent.nodes import chatbot
from app.ai_agent.tools import ALL_TOOLS
 
tool_node = ToolNode(ALL_TOOLS)
 
builder = StateGraph(AgentState)
 
builder.add_node("chatbot", chatbot)
builder.add_node("tools", tool_node)
 
builder.set_entry_point("chatbot")
 
# After the chatbot responds: if it asked for a tool call, go run the tool;
# otherwise the turn is done.
builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    {"tools": "tools", END: END},
)
 
# After a tool runs, hand control back to the chatbot so it can turn the
# tool result into a natural-language reply (or chain another tool call).
builder.add_edge("tools", "chatbot")
 
# In-memory checkpointer keyed by thread_id, so a rep's multi-turn
# conversation (e.g. "log a visit" -> "actually make that Negative sentiment")
# keeps context across HTTP requests.
checkpointer = MemorySaver()
 
agent_graph = builder.compile(checkpointer=checkpointer)