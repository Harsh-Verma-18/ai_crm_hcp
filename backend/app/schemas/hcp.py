from pydantic import BaseModel, EmailStr, ConfigDict
 
 
class HCPBase(BaseModel):
    name: str
    speciality: str
    hospital: str
    city: str
    email: EmailStr
    phone: str
 
 
class HCPCreate(HCPBase):
    pass
 
 
class HCPUpdate(HCPBase):
    pass
 
 
class HCPOut(HCPBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
 