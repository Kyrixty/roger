import os
import databases
import sqlalchemy

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(
    f"{os.path.abspath(os.path.dirname(__file__))}/../../.env"
)

hostname = os.environ.get("DATABASE_HOST_NAME")
username = os.environ.get("DATABASE_USERNAME")
password = os.environ.get("DATABASE_PASSWORD")
port = os.environ.get("DATABASE_SERVER_PORT")
name = os.environ.get("DATABASE_NAME")
ssl = os.environ.get("DATABASE_SSL_MODE")

SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{hostname}:{port}/{name}?sslmode={ssl}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_size=3,
    max_overflow=0,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    '''Yields a DB. VERY useful for API endpoints as it allows them to access the database.'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()