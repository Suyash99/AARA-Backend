from datetime import datetime
from app.models.user import User
from app.mapper.user_request import UserRequest
from app.mapper.user_response import UserResponse
from app.utils.crypto_utils import PasswordUtils
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

        # image = getBytes(user.image_uri)

        return UserResponse(
                code=user.code,
                name=user.name,
                about=user.about,
                color=user.color,
                image=None,
                username=user.username,
            )
