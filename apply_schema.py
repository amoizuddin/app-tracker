from db.database import engine, metadata
from db.models import job_applications

metadata.create_all(bind=engine)