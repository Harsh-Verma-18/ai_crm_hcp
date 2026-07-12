from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.interaction import Interaction
from app.models.hcp import HCP
from app.schemas.interaction import InteractionCreate, InteractionUpdate, InteractionOut

router = APIRouter(prefix="/interactions", tags=["Interaction"])


@router.post("/", response_model=InteractionOut)
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    """Used by the structured form path of the Log Interaction screen."""
    hcp = db.query(HCP).filter(HCP.id == payload.hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")

    interaction = Interaction(**payload.model_dump())
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.get("/", response_model=list[InteractionOut])
def list_interactions(hcp_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Interaction).order_by(Interaction.id.desc())
    if hcp_id is not None:
        query = query.filter(Interaction.hcp_id == hcp_id)
    return query.all()


@router.get("/{interaction_id}", response_model=InteractionOut)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction


@router.put("/{interaction_id}", response_model=InteractionOut)
def update_interaction(
    interaction_id: int, payload: InteractionUpdate, db: Session = Depends(get_db)
):
    """Used by the structured 'Edit Interaction' form."""
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(interaction, field, value)

    db.commit()
    db.refresh(interaction)
    return interaction


@router.delete("/{interaction_id}")
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    db.delete(interaction)
    db.commit()
    return {"message": "Interaction deleted successfully"}