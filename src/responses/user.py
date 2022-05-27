from pydantic import BaseModel

class UserData(BaseModel):
    id: int
    username: str
    time_created: str
    authored_packages: list[int]