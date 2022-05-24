from fastapi import HTTPException

def MissingFieldsError(detail: str = "Missing fields!"):
    raise HTTPException(status_code=400, detail=detail)

def InvalidFieldsError(detail: str = "Invalid fields!"):
    raise HTTPException(status_code=400, detail=detail)

def InsufficientPermissionsError(detail: str = "You do not have the required permissions to perform this action!"):
    raise HTTPException(status_code=403, detail=detail)