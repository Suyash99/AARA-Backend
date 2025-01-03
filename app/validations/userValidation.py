from pydantic import BaseModel, EmailStr, field_validator, root_validator, model_validator
from app.models.User import User
from app.repository.userRepository import UserRepository
from app.exceptions.userException import UserExceptionError
from app.appConstants import USER_EXCEPTION_ERRORS

class UserValidation(User, BaseModel):
    email: EmailStr

    @model_validator(mode="before")
    def create_user_checks(self, data:User) -> User:
        UserValidation.validate_username(self, data.username)
        UserValidation.validate_unique_email(self, data.email)
        UserValidation.validate_unique_user_code(self, data.user_code)
        return data

    @field_validator("username")
    def validate_username(self, username: str):
        if len(username) < 3:
            raise UserExceptionError(USER_EXCEPTION_ERRORS['VALID_USERNAME'], "username")

    @field_validator("email")
    def validate_unique_email(self, value):
        if UserRepository.query_in_db(self, "email = ?", [value]).build().count() > 0:
            raise UserExceptionError(USER_EXCEPTION_ERRORS['VALID_UNIQUE_EMAIL'], "email")

    @field_validator("user_code")
    def validate_unique_user_code(self, value):
        if UserRepository.query_in_db(self, "user_code = ?", [value]).build().count() > 0:
            raise UserExceptionError(USER_EXCEPTION_ERRORS['VALID_UNIQUE_USER_CODE'], "user_code")
