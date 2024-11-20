from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from sqlalchemy import select, delete
from database import engine
from models import job_applications
from datetime import datetime
from typing import Literal

app = FastAPI()

#adding cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#request and response model
class JobApplication(BaseModel):
    company_name: str
    position: str
    date_applied: str
    status: Literal["Applied", "Interviewing", "Offer Received", "Rejected", "Ghosted"]
    notes: str = None

@app.get("/")
def root():
    return {"message": "Job Application Tracker API"}

@app.get("/applications/")
async def get_all_applications():
    query = select(job_applications)
    with engine.connect() as conn:
        results = conn.execute(query).mappings().all()
    return results

@app.get("/applications/{application_id}")
async def get_application(application_id: int):
    query = select(job_applications).where(job_applications.c.id == application_id)
    with engine.connect() as conn:
        result = conn.execute(query).mappings().first()
    if result is None:
        raise HTTPException(status_code=404, detail="Job Application not found")
    return dict(result)

@app.post("/applications/")
async def add_application(application: JobApplication):
    """
    Add a new job application.
    """
    try:
        # Convert date_applied to datetime object
        application_data = application.model_dump()
        application_data["date_applied"] = datetime.strptime(application.date_applied, "%Y-%m-%d")

        # Insert into the database
        query = job_applications.insert().values(**application_data)
        with engine.begin() as conn:  # Use begin() for context management
            conn.execute(query)
        return {"message": "Application added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/applications/{application_id}")
async def update_application(application: JobApplication, application_id: int):
    query = select(job_applications).where(job_applications.c.id == application_id)
    with engine.connect() as conn:
        result = conn.execute(query).mappings().first()
        if result == None:
            raise HTTPException(status_code=404, detail="job app not found")
        
    try:
        updated_data = application.model_dump()
        updated_data["date_applied"]= datetime.strptime(application.date_applied, "%Y-%m-%d")
        update_query = (
            job_applications.update()
            .where(job_applications.c.id == application_id)
            .values(**updated_data)
        )
        with engine.begin() as conn:
            conn.execute(update_query)
        return {"message": "Job App updated successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid date format use YYYY-MM-DD")
    
@app.delete("/applications/{application_id}")
async def delete_application(application_id: int):
    query = delete(job_applications).where(job_applications.c.id == application_id)

    with engine.begin() as conn:
        result = conn.execute(query)

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Job application with ID {application_id} not found"
        )
    return {"message": f"job application with ID {application_id} deleted successfully"}