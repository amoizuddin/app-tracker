from database import engine
from models import metadata

metadata.create_all(bind=engine)