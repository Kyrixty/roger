from fastapi import HTTPException

def UserValidateError(detail: str = "Bad user fields"):
    raise HTTPException(status_code=400, detail=detail)

def UserNotFoundError(detail: str = "Requested user could not be found!"):
    raise HTTPException(status_code=404, detail=detail)

def UserAlreadyExistsError(detail: str = "User already exists!"):
    raise HTTPException(status_code=409, detail=detail)

def BadCredentialsError(detail: str = "Bad username or password"):
    raise HTTPException(status_code=401, detail=detail)
