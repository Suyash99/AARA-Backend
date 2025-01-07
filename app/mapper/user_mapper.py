from app.models.user import User
from app.dto.request.user_request import UserRequest
from app.dto.response.user_response import UserResponse, UserResponseV2
from app.utils.crypto_utils import PasswordUtils
from typing import Optional
import time

class UserMapper:
    @staticmethod
    def to_user(request: UserRequest, image_url:Optional[str]):
        if request is None:
            return None

        hashed_password = PasswordUtils.hash_password(request.password)

        # If updated_at is not provided, use the current timestamp
        created_at = round(time.time() * 1000)
        updated_at = round(time.time() * 1000)

        return User(
            name=request.name,
            username=request.username,
            about=request.about,
            password=hashed_password,
            code=request.code,
            color=request.color,
            created_by=request.code,
            updated_by=request.code,
            created_at=created_at,
            updated_at=updated_at,
            image_uri=image_url
        )

    @staticmethod
    def to_user_response(user: User, include_pass:bool=False):
        if user is None:
            return None

        if not include_pass:
            return UserResponse(
                    code=user.code,
                    name=user.name,
                    about=user.about,
                    color=user.color
            )
        else:
            return UserResponseV2(
                code=user.code,
                name=user.name,
                about=user.about,
                color=user.color,
                password=user.password
            )