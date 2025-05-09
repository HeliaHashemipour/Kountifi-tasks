from enum import Enum
from sqlalchemy import Column, String, JSON, Enum as SQLEnum
from database import Base

class JobStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id = Column(String, primary_key=True, index=True)
    document = Column(JSON)
    status = Column(SQLEnum(JobStatus), default=JobStatus.UPLOADED)
    result = Column(JSON, nullable=True)