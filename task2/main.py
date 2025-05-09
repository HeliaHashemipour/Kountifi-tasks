from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import crud
import schemas
import asyncio
from database import get_db, engine
from typing import Dict, Any

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

## essential endpoints
@app.post("/upload")
async def upload_document(
    payload: Dict[str, Any],  
    db: Session = Depends(get_db)
):
    """Upload a JSON document (invoice or contract)"""
    db_job = crud.create_job(db, payload)  # Now stores the raw payload
    return {
        "job_id": db_job.id,
        "message": "Document uploaded successfully"
    }


@app.post("/process")
async def process_document(
    request: schemas.ProcessRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start processing an uploaded document"""
    db_job = crud.get_job(db, request.job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if db_job.status != schemas.JobStatus.UPLOADED:
        raise HTTPException(status_code=400, detail="Job already processed or processing")
    
    crud.update_job_status(db, request.job_id, schemas.JobStatus.PROCESSING)
    
    background_tasks.add_task(process_document_background, request.job_id, db)
    
    return {
        "job_id": request.job_id,
        "message": "Processing started"
    }


async def process_document_background(job_id: str, db: Session):
    """Background task that simulates processing"""
    await asyncio.sleep(2.5)  # Simulate processing time
    
    # Update job status
    crud.update_job_status(
        db,
        job_id,
        schemas.JobStatus.COMPLETED,
        {"message": "Processing completed successfully"}
    )



@app.get("/status/{job_id}")
async def get_status(
    job_id: str,
    db: Session = Depends(get_db)
):
    """Check processing status"""
    db_job = crud.get_job(db, job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    response = {
        "job_id": job_id,
        "status": db_job.status,
        "document_type": list(db_job.document.keys())[0] if db_job.document else "unknown"
    }
    
    if db_job.status == schemas.JobStatus.COMPLETED:
        response["result"] = db_job.result
    
    return response