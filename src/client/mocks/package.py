from pydantic import BaseModel

class PackageData(BaseModel):
    id: int
    title: str
    authors: list[int]

class PackageReference(BaseModel):
    id: int
    ref: str