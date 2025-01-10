
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobBase(BaseModel):
    title: str
    description: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: str
    recruiter_id: str
    created_at: datetime

    class Config:
        # This allows the model to work with MongoDB's _id field
        alias_generator = lambda x: f"_{x}" if x == "id" else x
        allow_population_by_field_name = True
        
class JobApplication(BaseModel):
    job_id: str
    candidate_id: str
    applied_at: datetime 