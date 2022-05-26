from pydantic import BaseModel

class PackageSchema(BaseModel):
    title: str