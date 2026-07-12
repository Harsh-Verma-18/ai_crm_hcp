from typing import Optional
from pydantic import BaseModel
 
 
class ChatRequest(BaseModel):
    message: str
    # lets the frontend keep the same LangGraph thread across turns
    thread_id: Optional[str] = "default"
 
 
class ChatResponse(BaseModel):
    answer: str
    thread_id: str
 