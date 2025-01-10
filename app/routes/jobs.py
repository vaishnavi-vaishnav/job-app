from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.job import JobCreate, Job
from app.utils.auth_utils import get_current_recruiter
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Job)
async def create_job(
    request: Request, 
    job: JobCreate, 
    current_user: str = Depends(get_current_recruiter)
):
    job_dict = job.dict()
    job_dict["_id"] = str(ObjectId())
    job_dict["created_at"] = datetime.utcnow()
    job_dict["recruiter_id"] = current_user
    
    await request.app.mongodb["jobs"].insert_one(job_dict)
    
    job_dict["id"] = job_dict.pop("_id")
    return job_dict

@router.get("/", response_model=list[Job])
async def list_jobs(request: Request):
    jobs = []
    cursor = request.app.mongodb["jobs"].find()
    async for job in cursor:
        job["id"] = str(job.pop("_id"))
        jobs.append(job)
    return jobs