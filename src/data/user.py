from pydantic import BaseModel
from email_validator import validate_email, EmailNotValidError

class UserAuthSchema(BaseModel):
    username: str
    password: str

    def validate(self) -> bool: ...

class UserLoginSchema(UserAuthSchema):
    def validate(self) -> bool:
        if not self.username or not self.password:
            return False
        return True

class UserSignupSchema(UserAuthSchema):
    email: str

    def validate(self) -> bool:
        if not self.username or not self.password:
            return False
        try:
            validate_email(self.email)
        except EmailNotValidError:
            return False
        return True