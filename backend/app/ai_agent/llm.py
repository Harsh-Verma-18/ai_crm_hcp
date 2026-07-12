import os
from langchain_groq import ChatGroq
 
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
 
# Primary conversational model: fast + cheap, drives the chat turn-by-turn
# and decides which tool to call. Required by the assignment spec.
llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "gemma2-9b-it"),
    temperature=0,
    api_key=GROQ_API_KEY,
)
 
# Larger-context fallback model. Used inside the `log_interaction` tool for
# structured extraction (summary / sentiment / entities) from long or messy
# free-text notes, where the bigger model is worth the extra latency.
llm_extraction = ChatGroq(
    model=os.getenv("GROQ_FALLBACK_MODEL", "llama-3.3-70b-versatile"),
    temperature=0,
    api_key=GROQ_API_KEY,
)
 