from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.job import JobApplication
from app.utils.auth_utils import get_current_candidate, get_current_recruiter
from app.services.email_service import send_application_emails
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/apply/{job_id}")
async def apply_to_job(
    request: Request,
    job_id: str,
    current_user: str = Depends(get_current_candidate)
):
    # Check if already applied
    existing_application = await request.app.mongodb["applications"].find_one({
        "job_id": job_id,
        "candidate_id": current_user
    })
    if existing_application:
        raise HTTPException(status_code=400, detail="Already applied to this job")
    
    # Get job details
    job = await request.app.mongodb["jobs"].find_one({"_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Create application
    application = {
        "_id": str(ObjectId()),
        "job_id": job_id,
        "candidate_id": current_user,
        "applied_at": datetime.utcnow()
    }
    await request.app.mongodb["applications"].insert_one(application)
    
       
    # Get recruiter details and send emails
    # recruiter = await request.app.mongodb["users"].find_one({"_id": job["recruiter_id"]})
    # send_application_emails(job["title"], user["email"], recruiter["email"])

    # Get recruiter details and send emails
    recruiter = await request.app.mongodb["users"].find_one({"_id": job["recruiter_id"]})
    candidate = await request.app.mongodb["users"].find_one({"_id": current_user})
 
    # Send application emails
    send_application_emails(job["title"], candidate["email"], recruiter["email"])
    
    return {"message": "Application submitted successfully"}

# Candidate can see all jobs they've applied for
@router.get("/my-applications")
async def get_my_applications(request: Request, current_user: str = Depends(get_current_candidate)):
    applications = []
    cursor = request.app.mongodb["applications"].find({"candidate_id": current_user})
    async for application in cursor:
        job = await request.app.mongodb["jobs"].find_one({"_id": application["job_id"]})
        applications.append({
            # "application": application,
            "job": job
        })
    return applications

# Recruiter an see all the applications for a job
@router.get("/job-applications/{job_id}")
async def get_job_applications(
    request: Request,
    job_id: str,
    current_user: str = Depends(get_current_recruiter)
):
    # Verify user is the recruiter who posted the job
    job = await request.app.mongodb["jobs"].find_one({"_id": job_id})
    if not job or job["recruiter_id"] != current_user:
        raise HTTPException(status_code=403, detail="Access denied")
    
    applications = []
    cursor = request.app.mongodb["applications"].find({"job_id": job_id})
    async for application in cursor:
        candidate = await request.app.mongodb["users"].find_one({"_id": application["candidate_id"]})
        applications.append({
            "application": application,
            "candidate": candidate
        })
        return applications 