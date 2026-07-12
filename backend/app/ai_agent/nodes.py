from langchain_core.messages import SystemMessage
from app.ai_agent.agent import tool_agent, SYSTEM_PROMPT


def chatbot(state):
    messages = state["messages"]

    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)

    response = tool_agent.invoke(messages)

   

    return {"messages": [response]}