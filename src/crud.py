'''
This file concerns database-related operations, such as committing users & problems to a database,
comparing passwords, fetching users & problems, etc.
'''

import binascii
import os

from models.user import User
from models.package import Package
from data.user import UserLoginSchema, UserSignupSchema
from data.package import PackageSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from passlib.hash import bcrypt
#from hashlib import sha256

def pass_hash(password: str, salt: str) -> str:
    '''Hashes a user's password given a salt.'''
    password += salt
    return bcrypt.hash(password)


def get_user(db: Session, user_id: int):
    '''Gets a user given a user's id. Returns `None` if the user does not exist.'''
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User:
    '''Gets a user given a user's username. Returns `None` if the user does not exist.'''
    return db.query(User).filter(User.username == username).first()


def match_password(db: Session, user: UserLoginSchema | UserSignupSchema) -> bool:
    '''Returns `True` if `user.password` matches the requested user's password. `False` otherwise.'''
    db_user = get_user_by_username(db=db, username=user.username)
    password = pass_hash(user.password, db_user.salt) # type: ignore
    if not db_user or bcrypt.verify(password, db_user.password): # type: ignore
        return False
    return True


def get_users(db: Session, skip: int = 0, limit: int = 100):
    '''Returns users from `skip`->`limit`.'''
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserSignupSchema, isAdmin: bool = False):
    '''Creates, adds, commits, and refreshes a user to the app's database. Returns the newly created user.'''
    salt = binascii.hexlify(os.urandom(32)).decode()
    password = pass_hash(user.password, salt)
    db_user = User(
        username=user.username, 
        password=password, 
        email=user.email,
        salt=salt,
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"User with email '{user.email}' already exists!")

    return db_user

def delete_user(user: User, db: Session):
    '''Deletes a problem from the database.'''
    db.delete(user)
    db.commit()


def get_pkg(db: Session, pid: int):
    '''Gets a user given a package's id. Returns `None` if the package does not exist.'''
    return db.query(Package).filter(Package.id == pid).first()


def get_pkg_by_title(db: Session, title: str) -> User:
    '''Gets a package given a package title. Returns `None` if the package does not exist.'''
    return db.query(Package).filter(Package.title == title).first()

def get_pkgs(db: Session, skip: int = 0, limit: int = 100):
    '''Returns users from `skip`->`limit`.'''
    return db.query(Package).offset(skip).limit(limit).all()


def create_pkg(db: Session, author: User, pkg: PackageSchema):
    '''Creates, adds, commits, and refreshes a package to the app's database. Returns the newly created package.'''
    package = Package(
        title=pkg.title, 
        author_list=[author.id],
    )
    try:
        db.add(package)
        db.commit()
        db.refresh(package)
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"Package with title '{pkg.title}' already exists!")
    return package

def delete_pkg(pkg: Package, db: Session):
    '''Deletes a problem from the database.'''
    db.delete(pkg)
    db.commit()