from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from uuid import UUID
import redis
from rq import Queue

from app.database import get_db
from app.models import Person
from app.services.research_agent import enrich_person

router = APIRouter()

redis_conn = redis.Redis(host='localhost', port=6379, db=0)
queue = Queue(connection=redis_conn)

@router.post("/enrich/{person_id}")
def enrich_person_endpoint(
    person_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    job = queue.enqueue(enrich_person, person_id)
    
    return {
        "message": "Enrichment job started",
        "job_id": job.id,
        "person_id": person_id
    }

@router.get("/job/{job_id}")
def get_job_status(job_id: str):
    job = queue.fetch_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job_id,
        "status": job.get_status(),
        "result": job.result if job.is_finished else None,
        "error": str(job.exc_info) if job.is_failed else None
    }