from fastapi import APIRouter
from langchain_core.messages import HumanMessage
 
from app.ai_agent.graph import agent_graph
from app.schemas.chat_schema import ChatRequest, ChatResponse
 
router = APIRouter()
 
 
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
 
    result = agent_graph.invoke(
        {"messages": [HumanMessage(content=request.message)]},
        config=config,
    )
 
    return ChatResponse(
        answer=result["messages"][-1].content,
        thread_id=request.thread_id,
    )
 