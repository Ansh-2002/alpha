import uuid
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id", ondelete="CASCADE"))
    name = Column(String)
    domain = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    campaign = relationship("Campaign", back_populates="companies")
    people = relationship("Person", back_populates="company", cascade="all, delete-orphan")
    context_snippets = relationship("ContextSnippet", 
                                   foreign_keys="ContextSnippet.entity_id",
                                   primaryjoin="and_(Company.id==ContextSnippet.entity_id, ContextSnippet.entity_type=='company')",
                                   cascade="all, delete-orphan")