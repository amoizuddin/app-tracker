from database import engine, metadata
from models import job_applications



metadata.create_all(bind=engine)
