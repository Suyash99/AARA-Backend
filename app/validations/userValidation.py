from pydantic import BaseModel, EmailStr, field_validator, model_validator
from app.repository.userRepository import UserRepository
from app.exceptions.userException import UserExceptionError
from app.appConstants import USER_EXCEPTION_ERRORS

class UserValidation(BaseModel):
    username: str
    email: EmailStr
    user_code: str

    @model_validator(mode="before")
    @classmethod
    def create_user_checks(cls, data):
        cls.validate_username(data.get("username"))
        cls.validate_unique_email(data.get("email"), data.get("repository"))
        cls.validate_unique_user_code(data.get("user_code"), data.get("repository"))
        return data

    @classmethod
    def validate_username(cls, username: str):
        if len(username) < 3:
            raise UserExceptionError(USER_EXCEPTION_ERRORS['VALID_USERNAME'], "username")

    @classmethod
    def validate_unique_email(cls, email: str, repository: UserRepository):
        if repository.query_in_db("email = ?", [email]).build().count() > 0:
            raise UserExceptionError(USER_EXCEPTION_ERRORS['VALID_UNIQUE_EMAIL'], "email")

    @classmethod
    def validate_unique_user_code(cls, user_code: str, repository: UserRepository):
        if repository.query_in_db("user_code = ?", [user_code]).build().count() > 0:
            raise UserExceptionError(USER_EXCEPTION_ERRORS['VALID_UNIQUE_USER_CODE'], "user_code")
