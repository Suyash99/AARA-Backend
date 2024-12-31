from pydantic import BaseModel, EmailStr, field_validator
from app.models.User import User
from objectbox import Box
from app.exceptions.userException import ValidationError

# Initialize the ObjectBox Box
user_box = Box(User)

class UserValidation(User, BaseModel):
    email: EmailStr

    @field_validator("username")
    def validate_username(cls, username: str):
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long", "username")

    @field_validator("email")
    def validate_unique_email(cls, value):
        if user_box.query("email = ?", [value]).build().count() > 0:
            raise ValidationError("Email must be unique", "email")

    @field_validator("user_code")
    def validate_unique_user_code(cls, value):
        if user_box.query("user_code = ?", [value]).build().count() > 0:
            raise ValidationError("User code must be unique", "user_code")
