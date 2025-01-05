from datetime import datetime
from app.models.user import User
from app.mapper.userRequest import UserRequest
from app.mapper.userResponse import UserResponse
from app.utils.passwordUtils import PasswordUtils
import time

class UserMapper:
    @staticmethod
    def to_user(request: UserRequest):
        if request is None:
            return None

        hashed_password = PasswordUtils.hash_password(request.password)

        # If updated_at is not provided, use the current timestamp
        created_at = request.created_at if request.created_at else round(time.time() * 1000)
        updated_at = request.updated_at if request.updated_at else round(time.time() * 1000)

        return User(
            username=request.username,
            email=request.email,
            password=hashed_password,
            user_code=request.user_code,
            colour_code=request.colour_code,
            created_at=created_at,
            updated_at=updated_at,
            user_photo_bytes=request.user_photo_bytes
        )

    @staticmethod
    def to_user_response(user: User):
        if user is None:
            return None

        return UserResponse(
                id=user.id,
                user_code=user.user_code,
                colour_code=user.colour_code,
                user_photo_bytes=user.user_photo_bytes,
                username=user.username,
                email=user.email,
                password=user.password,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
