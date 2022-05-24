"""
Auth-related routes, such as /auth/login and /auth/signup are defined and handled here.
These routes are to be fetched via the frontend to handle retrieving valid JWT tokens, which
all protected routes (routes that require the user to be authorized) require.
"""

from os import access
import crud

from data.user import UserLoginSchema, UserSignupSchema
from utils.user import (
    GetUserIfTheyExist,
    EnsureUserIsAdmin,
    EnsureUserDoesNotExist,
)
from types.jwt import JWT
from responses.auth import AuthResponse, RefreshTokenResponse
from fastapi import HTTPException, Depends, APIRouter
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from database.sqlite import get_db
from exceptions.user import (
    UserValidateError,
    BadCredentials,
    UserAlreadyExistsError,
)

router = APIRouter(prefix="/auth")

# provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
@router.post("/login", response_model=AuthResponse)
def login(
    user: UserLoginSchema, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)
):
    """Handles account login"""
    if not user.validate():
        UserValidateError()
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if not db_user or not crud.match_password(db=db, user=user):
        BadCredentials()

    # Create JWT access + refresh tokens calculated with the user's username.
    access_token = Authorize.create_access_token(subject=user.username, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    jwt = JWT(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    auth_response = AuthResponse(
        uuid=db_user.id,  # type: ignore,
        username=db_user.username,  # type: ignore
        token=jwt,
    )
    return auth_response


@router.post("/signup", response_model=AuthResponse)
def signup(
    user: UserSignupSchema,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    """Handles account signup"""
    if not user.validate():
        UserValidateError()
    EnsureUserDoesNotExist(db, user.username)
    db_user = crud.create_user(db=db, user=user)
    access_token = Authorize.create_access_token(subject=user.username, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    auth_response = AuthResponse(
        uuid=db_user.id,  # type: ignore
        username=db_user.username,  # type: ignore
        token=JWT(access_token=access_token, refresh_token=refresh_token),
    )
    return auth_response


@router.post("/admin/create")
def createAdminAccount(
    user: UserSignupSchema,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    """Handles admin account creation"""
    Authorize.jwt_required()
    username = Authorize.get_jwt_subject()
    admin = GetUserIfTheyExist(db=db, username_or_uuid=username)
    EnsureUserIsAdmin(admin)
    new_admin = crud.get_user_by_username(db=db, username=user.username)
    if new_admin:
        UserAlreadyExistsError()

    new_admin = crud.create_user(db=db, user=user)
    new_admin.state = UserState(isAdmin=True).json()  # type: ignore
    db.commit()
    access_token = Authorize.create_access_token(subject=user.username, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    auth_response = AuthResponse(
        uuid=new_admin.id,  # type: ignore
        username=new_admin.username,  # type: ignore
        token=JWT(
            access_token=access_token,
            refresh_token=refresh_token,
        ),
    )
    return auth_response


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh(Authorize: AuthJWT = Depends()):
    """
    This endpoint will refresh a user's access token.
    Note: this endpoint REQUIRES a valid refresh token to be provided.
    All new access tokens generated will be non-fresh access tokens.
    """

    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    if not current_user:
        raise HTTPException(status_code=404, detail="Refresh token is invalid.")
    new_access_token = Authorize.create_access_token(subject=current_user, fresh=False)
    access_token_response = RefreshTokenResponse(access_token=new_access_token)
    return access_token_response
