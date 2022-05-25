from pydantic import BaseModel
from data.jwt import JWT

class AuthResponse(BaseModel):
    uuid: int
    username: str
    token: JWT

class RefreshTokenResponse(BaseModel):
    access_token: str