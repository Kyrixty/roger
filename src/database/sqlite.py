'''
This file concerns database setup, as well as defining the useful get_db() function
which is a dependency needed for auth-related routes such as login and signup.
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./vcoj.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db" 
# # When migrating to Postgres just uncomment this line.
# and adapt it with your database data and credentials (equivalently for MySQL, MariaDB or any other).

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
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