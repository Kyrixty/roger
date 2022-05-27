import requests
import json

from mocks.jwt import JWT
from mocks.user import UserData
from mocks.package import PackageReference, PackageData

headers = {
    "Content-Type": "application/json"
}

def login(username: str, password: str) -> JWT | None:
    payload = json.dumps({
        "username": username,
        "password": password,
    })
    r = requests.post("http://localhost:8000/auth/login", headers=headers, data=payload)
    content = json.loads(r.content.decode())
    try:
        return JWT(
            access_token=content["token"]["access_token"],
            refresh_token=content["token"]["refresh_token"],
        )
    except KeyError: ...

def signup(username: str, password: str, email: str) -> JWT | None:
    payload = json.dumps({
        "username": username,
        "password": password,
        "email": email,
    })

    r = requests.post("http://localhost:8000/auth/signup", headers=headers, data=payload)
    content = json.loads(r.content.decode())
    try:
        return JWT(
            access_token=content["token"]["access_token"],
            refresh_token=content["token"]["refresh_token"],
        )
    except KeyError: ...

def getUser(uuid: int, token: JWT) -> UserData | None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token.access_token}",
    }

    r = requests.get(f"http://localhost:8000/user/{uuid}", headers=headers)
    content = json.loads(r.content.decode())
    try:
        return UserData(
            id=content["id"],
            username=content["username"],
            time_created=content["time_created"],
            authored_packages=content["authored_packages"],
        )
    except KeyError: ...

def getPackage(pid: int, token: JWT):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token.access_token}",
    }

    r = requests.get(f"http://localhost:8000/package/{pid}", headers=headers)
    content = json.loads(r.content.decode())
    try:
        return PackageData(
            id=content["id"],
            title=content["title"],
            authors=content["authors"],
        )
    except KeyError: ...


def createPackage(title: str, token: JWT) -> PackageReference | None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token.access_token}",
    }

    payload = json.dumps({
        "title": title
    })

    r = requests.post("http://localhost:8000/package/create", headers=headers, data=payload)
    content = json.loads(r.content.decode())
    try:
        return PackageReference(
            id=content["id"],
            ref=content["ref"],
        )
    except KeyError: ...

if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    token = signup(username, password, email)
    token = login(username, password)

    if token:
        ref = createPackage("4th package", token)
        user = getUser(1, token)
        pkg = getPackage(ref.id, token) # type: ignore
        print(ref)
        print(user)
        print(pkg)