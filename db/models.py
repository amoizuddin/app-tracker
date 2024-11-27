from sqlalchemy import Table, Column, Integer, String, DateTime, create_engine
from database import metadata

job_applications = Table(
    "job_applications",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("company_name", String, nullable=False),
    Column("position", String, nullable=False),
    Column("date_applied", DateTime),
    Column("status", String, nullable=False, default="Applied"),
    Column("notes", String)
)