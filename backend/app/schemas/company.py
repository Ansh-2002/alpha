from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None

class CompanyCreate(CompanyBase):
    campaign_id: UUID

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None

class Company(CompanyBase):
    id: UUID
    campaign_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True