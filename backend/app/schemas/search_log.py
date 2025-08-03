from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Dict, Any

class SearchLogBase(BaseModel):
    context_snippet_id: UUID
    iteration: int
    query: str
    top_results: Dict[str, Any]

class SearchLogCreate(SearchLogBase):
    pass

class SearchLog(SearchLogBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True