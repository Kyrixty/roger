import crud

from sqlalchemy.orm import Session
from utils.package import EnsurePackageDoesNotExist, GetPackageIfItExists
from utils.user import GetUserIfTheyExist
from responses.package import PackageData, PackageReference
from data.package import PackageSchema
from database.postgresql import get_db
from fastapi import APIRouter, Depends, Request
from fastapi_jwt_auth import AuthJWT

router = APIRouter(
    prefix="/package"
)

@router.get("/{pid}")
def getPackage(
    pid: int, 
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    pkg = GetPackageIfItExists(db, pid)
    return PackageData(
        id=pkg.id,
        title=pkg.title,
        authors=pkg.author_list,
    )

@router.post("/create", response_model=PackageReference)
def createPackage(
    package: PackageSchema,
    request: Request,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    user = GetUserIfTheyExist(db, Authorize.get_jwt_subject())
    EnsurePackageDoesNotExist(db, package.title)
    pkg = crud.create_pkg(db, user, package)
    user.author_package(pkg.id, db) # type: ignore
    refUrl = request.url._url.replace("create", f"{pkg.id}")
    return PackageReference(
        id=pkg.id,
        ref=refUrl,
    )