#type: ignore
'''
Models are database models. They are "blueprints" for storing data in our app's database.
'''
from email.policy import default
import json

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey, 
    Integer, 
    String, 
    JSON, 
    DateTime,
    PickleType,
)
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from database.sqlite import Base

__all__ = ("User", "Problem",)

class User(Base):
    '''The User database model. All fields for each User in the database are specified here.'''
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    isAdmin = Column(Boolean, index=True, default=False)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    salt = Column(String, unique=True, index=False)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())