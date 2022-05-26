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

__all__ = ("Package",)

mList = MutableList.as_mutable(PickleType)

class Package(Base):
    __tablename__ = "package"
    id: int = Column(Integer, primary_key=True, index=True) 
    title: str = Column(String, index=True, unique=True)
    author_list: list[int] = Column(mList, default=[])
    subscriptions: list[int] = Column(mList, default=[])