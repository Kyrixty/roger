import crud

from models.package import Package
from exceptions.http import (
    InvalidFieldsError, 
    InsufficientPermissionsError,
)
from exceptions.package import (
    PackageAlreadyExistsError, 
    PackageNotFoundError,
)
from sqlalchemy.orm import Session


def GetPackageIfItExists(db: Session, title_or_pid: str | int | None, error_on_not_found: bool = True) -> Package:
    if isinstance(title_or_pid, str):
        package = crud.get_pkg_by_title(db=db, title=title_or_pid)
        if not package and error_on_not_found:
            PackageNotFoundError(f"Package with title '{title_or_pid}' could not be found!")
    elif isinstance(title_or_pid, int):
        package = crud.get_pkg(db=db, pid=title_or_pid)
        if not package and error_on_not_found:
            PackageNotFoundError(f"Package with PID '{title_or_pid}' could not be found!")
    else:
        InvalidFieldsError()
    return package

def EnsurePackageDoesNotExist(db: Session, title_or_pid: str | int | None):
    package = GetPackageIfItExists(db=db, title_or_pid=title_or_pid, error_on_not_found=False)
    if package:
        if isinstance(title_or_pid, str):
            PackageAlreadyExistsError(f"Package with title '{title_or_pid}' already exists!")
        PackageAlreadyExistsError(f"Package with PID {title_or_pid} already exists!")