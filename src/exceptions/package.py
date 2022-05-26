from fastapi import HTTPException

def PackageNotFoundError(detail: str = "Package could not be found!"):
    raise HTTPException(status_code=404, detail=detail)

def PackageAlreadyExistsError(detail: str = "Package already exists!"):
    raise HTTPException(status_code=409, detail=detail)