import uuid
from sqlalchemy import Column, String, DateTime, func, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import Base

class SearchLog(Base):
    __tablename__ = "search_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    context_snippet_id = Column(UUID(as_uuid=True), ForeignKey("context_snippets.id", ondelete="CASCADE"))
    iteration = Column(Integer)
    query = Column(String)
    top_results = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    context_snippet = relationship("ContextSnippet", back_populates="search_logs")