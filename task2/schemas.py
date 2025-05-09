from pydantic import BaseModel
from enum import Enum
from typing import Optional, Dict, Any

class JobStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class DocumentUpload(BaseModel):
    data: Dict[str, Any]

class ProcessRequest(BaseModel):
    job_id: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    document_type: str
    result: Optional[Dict[str, Any]] = None