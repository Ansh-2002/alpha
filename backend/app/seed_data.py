from app.database import SessionLocal
from app.models import Campaign, Company, Person

def seed_database():
    db = SessionLocal()
    try:
        existing_campaign = db.query(Campaign).first()
        if existing_campaign:
            print("Database already seeded")
            return
        
        campaign = Campaign(
            name="Alpha Research Campaign",
            status="active"
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        
        company = Company(
            campaign_id=campaign.id,
            name="TechCorp",
            domain="techcorp.com"
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        
        person1 = Person(
            company_id=company.id,
            full_name="John Smith",
            email="john.smith@techcorp.com",
            title="CEO"
        )
        
        person2 = Person(
            company_id=company.id,
            full_name="Sarah Johnson",
            email="sarah.johnson@techcorp.com", 
            title="CTO"
        )
        
        db.add(person1)
        db.add(person2)
        db.commit()
        
        print("Database seeded successfully!")
        print(f"Campaign: {campaign.name}")
        print(f"Company: {company.name}")
        print(f"People: {person1.full_name}, {person2.full_name}")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()