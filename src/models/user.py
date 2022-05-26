# type: ignore
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
from database.postgresql import Base
from data.package import PackageSchema

__all__ = ("User",)

mList = MutableList.as_mutable(PickleType)
class User(Base):
    '''The User database model. All fields for each User in the database are specified here.'''
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True, index=True)
    isAdmin: bool = Column(Boolean, index=True, default=False)
    username: str = Column(String, unique=True, index=True)
    email: str = Column(String, unique=True, index=True)
    password: str = Column(String)
    salt: str = Column(String, unique=True, index=False)

    time_created: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    time_updated: DateTime = Column(DateTime(timezone=True), onupdate=func.now())

    authored_packages: list[int] = Column(mList, default=[])
    subscribed_packages: list[int] = Column(mList, default=[])

    def author_package(self, pid: int, db: Session):
        self.authored_packages.append(pid)
        db.commit()
        db.refresh(self)