from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./job_applications.db" #replace with postgres DB
engine = create_engine(DATABASE_URL)
metadata = MetaData()
