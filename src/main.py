import sys

from fastapi import FastAPI, Request
from pydantic import BaseModel
from decouple import config
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from database.sqlite import engine
from models.user import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

class AuthSettings(BaseModel):
    authjwt_secret_key: str | bool = config("SECRET")
    authjwt_access_token_expires: int = 60*60 # 1 hour (60s*60min)

# Load config callback
@AuthJWT.load_config #type: ignore
def get_config():
    return AuthSettings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    '''Returned when a User's JWT access token expires (or their Authorization header is invalid due to some other reason).'''
    return JSONResponse(
        status_code=exc.status_code, #type: ignore
        content={"detail": exc.message} #type: ignore
    )