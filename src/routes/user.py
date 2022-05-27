from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from database.postgresql import get_db
from sqlalchemy.orm import Session
from responses.user import UserData
from utils.user import GetUserIfTheyExist

router = APIRouter(
    prefix="/user"
)

@router.get("/{uuid}", response_model=UserData)
def getUser(
    uuid: int,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    user = GetUserIfTheyExist(db, uuid)
    return UserData(
        id=user.id,
        username=user.username,
        time_created=str(user.time_created),
        authored_packages=user.authored_packages,
    )