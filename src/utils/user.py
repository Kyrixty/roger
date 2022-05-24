import crud

from models.user import User
from exceptions.http import (
    InvalidFieldsError, 
    InsufficientPermissionsError,
)
from exceptions.user import UserAlreadyExistsError, UserNotFoundError
from sqlalchemy.orm import Session


def GetUserIfTheyExist(db: Session, username_or_uuid: str | int | None, error_on_not_found: bool = True) -> User:
    if isinstance(username_or_uuid, str):
        user = crud.get_user_by_username(db=db, username=username_or_uuid)
        if not user and error_on_not_found:
            UserNotFoundError(f"User with username '{username_or_uuid} could not be found!")
    elif isinstance(username_or_uuid, int):
        user = crud.get_user(db=db, user_id=username_or_uuid)
        if not user and error_on_not_found:
            UserNotFoundError(f"User with UUID {username_or_uuid} could not be found!")
    else:
        InvalidFieldsError()
    return user

def EnsureUserIsAdmin(user: User):
    if not user.isAdmin:
        InsufficientPermissionsError()

def EnsureUserDoesNotExist(db: Session, username_or_uuid: str | int | None):
    user = GetUserIfTheyExist(db=db, username_or_uuid=username_or_uuid)
    if user:
        UserAlreadyExistsError()