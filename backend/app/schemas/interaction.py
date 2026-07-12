from typing import Optional
from pydantic import BaseModel, ConfigDict
 
 
class InteractionCreate(BaseModel):
    """Payload sent by the structured form (or by the log_interaction tool)."""
 
    hcp_id: int
    interaction_type: str
    products_discussed: Optional[str] = None
    raw_input: Optional[str] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    next_action: Optional[str] = None
    followup_date: Optional[str] = None
 
 
class InteractionUpdate(BaseModel):
    """Partial update payload used by the edit form / edit_interaction tool."""
 
    interaction_type: Optional[str] = None
    products_discussed: Optional[str] = None
    raw_input: Optional[str] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    next_action: Optional[str] = None
    followup_date: Optional[str] = None
 
 
class InteractionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    hcp_id: int
    interaction_type: Optional[str] = None
    products_discussed: Optional[str] = None
    raw_input: Optional[str] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    next_action: Optional[str] = None
    followup_date: Optional[str] = None