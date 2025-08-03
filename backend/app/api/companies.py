from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models import Company, ContextSnippet
from app.schemas import company as schemas
from app.schemas import context_snippet as snippet_schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Company])
def get_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()

@router.get("/{company_id}", response_model=schemas.Company)
def get_company(company_id: UUID, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.post("/", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.get("/{company_id}/snippets", response_model=List[snippet_schemas.ContextSnippet])
def get_company_snippets(company_id: UUID, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    snippets = db.query(ContextSnippet).filter(
        ContextSnippet.entity_id == company_id,
        ContextSnippet.entity_type == "company"
    ).all()
    return snippets