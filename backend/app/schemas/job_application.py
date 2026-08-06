from pydantic import BaseModel,ConfigDict,Field
from typing import Optional
from datetime import datetime,date
from app.enums import JobStatus

class createJob(BaseModel):
    role :str
    status : JobStatus = JobStatus.APPLIED
    applied_date : date = Field(default_factory=date.today)
    company : str
    job_url : str
    location : str
    notes : Optional[str] = None

class jobOut(BaseModel):
    id : int
    role : str
    status : str
    applied_date : date

    company : str
    job_url : str
    location : str
    notes : Optional[str] = None
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

class UpdateJob(BaseModel):
    role : Optional[str]=None
    role: Optional[str] = None
    status: JobStatus| None = None
    applied_date: Optional[date] = None
    company: Optional[str] = None
    job_url: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None