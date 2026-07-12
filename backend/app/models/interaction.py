from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
 
 
class Interaction(Base):
    """
    A single logged touchpoint between a field rep and an HCP.
 
    `raw_input` preserves exactly what the user typed/dictated (structured form
    notes or free-form chat message) so the AI-derived fields can always be
    re-generated or audited later. The AI-derived fields (summary, sentiment,
    next_action, followup_date, products_discussed) are filled in either by the
    LangGraph `log_interaction` tool (chat mode) or directly by the user via the
    structured form.
    """
 
    __tablename__ = "interactions"
 
    id = Column(Integer, primary_key=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=False)
 
    interaction_type = Column(String)       # e.g. "Visit", "Call", "Email", "Conference"
    products_discussed = Column(String)     # comma separated product names
    raw_input = Column(Text)                # original free-text notes / chat message
    summary = Column(Text)                  # AI-generated or user-provided summary
    sentiment = Column(String)              # Positive / Neutral / Negative
    next_action = Column(String)            # recommended / chosen next step
    followup_date = Column(String)          # ISO date string, nullable
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
 
    hcp = relationship("HCP", back_populates="interactions")