from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Dict, List, Any

class ContextSnippetBase(BaseModel):
    entity_type: str
    entity_id: UUID
    snippet_type: str = "research"
    payload: Dict[str, Any]
    source_urls: List[str]

class ContextSnippetCreate(ContextSnippetBase):
    pass

class ContextSnippet(ContextSnippetBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True