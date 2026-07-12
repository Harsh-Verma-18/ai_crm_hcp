from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
 
 
class FollowUp(Base):
    __tablename__ = "followups"
 
    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"))
    task = Column(String)
    due_date = Column(Date)
    status = Column(String, default="Pending")
 
    hcp = relationship("HCP", back_populates="followups")
 