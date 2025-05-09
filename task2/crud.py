from sqlalchemy.orm import Session
from models import ProcessingJob
import uuid

def create_job(db: Session, document: dict):
    job_id = str(uuid.uuid4())
    db_job = ProcessingJob(
        id=job_id,
        document=document,
        status="uploaded"
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job(db: Session, job_id: str):
    return db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()

def update_job_status(db: Session, job_id: str, status: str, result: dict = None):
    db_job = get_job(db, job_id)
    if db_job:
        db_job.status = status
        if result:
            db_job.result = result
        db.commit()
        db.refresh(db_job)
    return db_job