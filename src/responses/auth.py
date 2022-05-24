from pydantic import BaseModel
from types.jwt import JWT

class AuthResponse(BaseModel):
    uuid: int
    username: str
    token: JWT

class RefreshTokenResponse(BaseModel):
    access_token: str