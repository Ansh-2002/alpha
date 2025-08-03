import uuid
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class Person(Base):
    __tablename__ = "people"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    full_name = Column(String)
    email = Column(String, unique=True)
    title = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    company = relationship("Company", back_populates="people")
    context_snippets = relationship("ContextSnippet", 
                                   foreign_keys="ContextSnippet.entity_id",
                                   primaryjoin="and_(Person.id==ContextSnippet.entity_id, ContextSnippet.entity_type=='person')",
                                   cascade="all, delete-orphan")