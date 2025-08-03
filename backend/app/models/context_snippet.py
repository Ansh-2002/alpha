import uuid
from sqlalchemy import Column, String, DateTime, func, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import Base

class ContextSnippet(Base):
    __tablename__ = "context_snippets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String, nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    snippet_type = Column(String, default="research")
    payload = Column(JSONB, nullable=False)
    source_urls = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    search_logs = relationship("SearchLog", back_populates="context_snippet", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint(entity_type.in_(["company", "person"]), name="valid_entity_type"),
    )