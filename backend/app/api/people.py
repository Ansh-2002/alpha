from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models import Person
from app.schemas import person as schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Person])
def get_people(db: Session = Depends(get_db)):
    return db.query(Person).all()

@router.get("/{person_id}", response_model=schemas.Person)
def get_person(person_id: UUID, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.post("/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person