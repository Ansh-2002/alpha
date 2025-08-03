import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Campaign, Company, Person, ContextSnippet
from app.services.research_agent import DeepResearchAgent

@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///test.db")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield SessionLocal
    
    Base.metadata.drop_all(bind=engine)

class TestIntegration:
    def test_full_enrichment_flow(self, test_db):
        db = test_db()
        
        try:
            campaign = Campaign(name="Test Campaign", status="active")
            db.add(campaign)
            db.commit()
            db.refresh(campaign)
            
            company = Company(
                campaign_id=campaign.id,
                name="TestCorp",
                domain="testcorp.com"
            )
            db.add(company)
            db.commit()
            db.refresh(company)
            
            person = Person(
                company_id=company.id,
                full_name="John Doe",
                email="john@testcorp.com",
                title="CEO"
            )
            db.add(person)
            db.commit()
            db.refresh(person)
            
            agent = DeepResearchAgent()
            
            db.close()
            
            result = agent.enrich_person(person.id)
            
            assert result["success"] == True
            assert "snippet_id" in result
            
            db = test_db()
            snippet = db.query(ContextSnippet).filter(
                ContextSnippet.entity_id == company.id,
                ContextSnippet.entity_type == "company"
            ).first()
            
            assert snippet is not None
            assert snippet.payload is not None
            assert "company_value_prop" in snippet.payload
            
        finally:
            db.close()