
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobCreate(BaseModel):
    title: str
    description: str
    url: str

    class Config:
        populate_by_name = True  # Use the new key instead of the deprecated one

class Job(JobCreate):
    id: str
    recruiter_id: str
    created_at: datetime

    class Config:
        orm_mode = True
        populate_by_name = True  # Use the new key here as well
        
        
# class JobBase(BaseModel):
#     title: str
#     description: str

# class JobCreate(JobBase):
#     pass

# class Job(JobBase):
#     id: str
#     recruiter_id: str
#     created_at: datetime

#     class Config:
#         # This allows the model to work with MongoDB's _id field
#         alias_generator = lambda x: f"_{x}" if x == "id" else x
#         allow_population_by_field_name = True
        
class JobApplication(BaseModel):
    job_id: str
    candidate_id: str
    applied_at: datetime 