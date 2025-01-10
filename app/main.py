from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.routes import auth, jobs, applications
from app.config import settings
import certifi

app = FastAPI(title="Job Board API")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.mongodb_url,  # MongoDB connection string
        tls=True,  # Enable SSL
        tlsCAFile=certifi.where())
    app.mongodb = app.mongodb_client[settings.database_name]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(applications.router, prefix="/applications", tags=["Applications"]) 