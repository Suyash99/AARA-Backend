from datetime import datetime
from app.models.User import User
from app.mapper.userRequest import UserRequest
from app.mapper.userResponse import UserResponse
from app.utils.generateCodeForId import GenerateCodeForId
from app.utils.passwordUtils import PasswordUtils

class UserMapper:
    @staticmethod
    def to_user(request: UserRequest):
        if request is None:
            return None

        hashed_password = PasswordUtils.hash_password(request.password)
        generated_user_code = GenerateCodeForId.generate_random_code(6)
        # If updated_at is not provided, use the current timestamp
        updated_at = request.updated_at if request.updated_at else datetime

        return User(
            username=request.username,
            email=request.email,
            password=hashed_password,
            user_code=generated_user_code,
            colour_code=request.colour_code,
            created_at=datetime,
            updated_at=updated_at
        )

    @staticmethod
    def to_user_response(user: User):
        if user is None:
            return None

        return UserResponse(
            id=user.id,
            user_code=user.user_code,
            colour_code=user.colour_code,
            username=user.username,
            email=user.email,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
