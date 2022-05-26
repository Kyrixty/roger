import crud
import sys

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from decouple import config
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from database.postgresql import engine
from auth import auth
from models.user import Base
from routes import package

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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Roger API Documentation",
        version="1.4.1",
        description="This page describes each publicly available route and how to interact with them through your own applications.",
        routes=app.routes,
    )

    # Custom documentation fastapi-jwt-auth
    headers = {
        "name": "Authorization",
        "in": "header",
        "required": True,
        "schema": {
            "title": "Authorization",
            "type": "string"
        },
    }

    # Get routes from index 4 because before that fastapi define router for /openapi.json, /redoc, /docs, etc
    # Get all router where operation_id is authorize
    router_authorize = [route for route in app.routes[4:] if route.operation_id == "auth"] # type: ignore

    for route in router_authorize:
        method = list(route.methods)[0].lower() # type: ignore
        try:
            # If the router has another parameter
            openapi_schema["paths"][route.path][method]['parameters'].append(headers) # type: ignore
        except Exception:
            # If the router doesn't have a parameter
            openapi_schema["paths"][route.path][method].update({"parameters":[headers]}) # type: ignore

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(auth.router)
app.include_router(package.router)