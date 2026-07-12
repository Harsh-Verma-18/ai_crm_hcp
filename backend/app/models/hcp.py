from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
 
 
class HCP(Base):
    """A Healthcare Professional (doctor) that a field rep engages with."""
 
    __tablename__ = "hcps"
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    speciality = Column(String)
    hospital = Column(String)
    city = Column(String)
    email = Column(String)
    phone = Column(String)
 
    interactions = relationship(
        "Interaction", back_populates="hcp", cascade="all, delete-orphan"
    )
    followups = relationship(
        "FollowUp", back_populates="hcp", cascade="all, delete-orphan"
    )
 