from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.hcp import HCP
from app.schemas.hcp import HCPCreate, HCPUpdate, HCPOut

router = APIRouter(prefix="/hcps", tags=["HCP"])


@router.post("/", response_model=HCPOut)
def create_hcp(hcp: HCPCreate, db: Session = Depends(get_db)):
    new_hcp = HCP(**hcp.model_dump())
    db.add(new_hcp)
    db.commit()
    db.refresh(new_hcp)
    return new_hcp


@router.get("/", response_model=list[HCPOut])
def get_all_hcps(db: Session = Depends(get_db)):
    return db.query(HCP).all()


@router.get("/{hcp_id}", response_model=HCPOut)
def get_hcp_by_id(hcp_id: int, db: Session = Depends(get_db)):
    doctor = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.put("/{hcp_id}", response_model=HCPOut)
def update_hcp(hcp_id: int, hcp: HCPUpdate, db: Session = Depends(get_db)):
    doctor = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    for field, value in hcp.model_dump().items():
        setattr(doctor, field, value)

    db.commit()
    db.refresh(doctor)
    return doctor


@router.delete("/{hcp_id}")
def delete_hcp(hcp_id: int, db: Session = Depends(get_db)):
    doctor = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db.delete(doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}