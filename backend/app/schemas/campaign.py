from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List

class CampaignBase(BaseModel):
    name: str
    status: str = "draft"

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None

class Campaign(CampaignBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True