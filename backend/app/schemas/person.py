from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class PersonBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    title: Optional[str] = None

class PersonCreate(PersonBase):
    company_id: UUID

class PersonUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    title: Optional[str] = None

class Person(PersonBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True