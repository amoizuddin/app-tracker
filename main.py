from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from database import engine
from models import job_applications

app = FastAPI()

#request and response model
class JobApplication(BaseModel):
    company_name: str
    position: str
    date_applied: str
    status: str = "Applied"
    notes: str = None

@app.get("/")
def root():
    return {"message": "Job Application Tracker API"}

@app.get("/applications/")
async def get_all_applications():
    query = select(job_applications)
    with engine.connect() as conn:
        results = conn.execute(query).fetchall()
    return [dict(result) for result in results]

@app.get("/applications/{application_id}")
async def get_application(application_id: int):
    query = select(job_applications).where(job_applications.c.id == application_id)
    with engine.connect() as conn:
        result = conn.execute(query).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Job Application not found")
    return dict(result)

@app.post("/applications/")
async def add_application(application: JobApplication):
    query = job_applications.insert().values(**application.model_dump())
    with engine.connect() as conn:
        conn.execute(query)
    return {"message": "Job App added successfully"}

@app.put("/applications/{application_id}")
async def update_application(application: JobApplication, application_id: int):
    query = select(job_applications).where(job_applications.c.id == application_id)
    with engine.connect() as conn:
        result = conn.execute(query).fetchone()
        if result == None:
            raise HTTPException(status_code=404, detail="job app not found")
        
        update_query = (
            job_applications.update()
            .where(job_applications.c.id == application_id)
            .values(**application.model_dump())
        )
        conn.execute(update_query)
    return {"message": "Job App updated successfully"}