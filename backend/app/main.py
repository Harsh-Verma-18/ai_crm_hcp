import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from app.database import engine, Base
from app.models import hcp, hospital, product, interaction, followup  # noqa: F401 (needed for create_all)
from app.api.hcp import router as hcp_router
from app.api.interaction import router as interaction_router
from app.routers import ai
 
Base.metadata.create_all(bind=engine)
 
app = FastAPI(title="AI CRM HCP", version="1.0.0")
 
origins = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173").split(",")
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.include_router(hcp_router)
app.include_router(interaction_router)
app.include_router(ai.router, prefix="/ai", tags=["AI Agent"])
 
 
@app.get("/")
def home():
    return {"message": "AI CRM Backend Running"}