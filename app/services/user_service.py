from typing import List, Optional
from app.exceptions.response_exception import ResponseException
from app.exceptions.user_exception import UserExceptionError
from app.mapper.user_mapper import UserMapper
from app.dto.request.user_request import UserRequest
from app.dto.response.user_response import UserResponse
from app.repository.user_repository import UserRepository
from app.utils.constants import UPLOAD_DIR
from app.utils.crypto_utils import PasswordUtils
from app.utils.generateCodeForId import GenerateCodeForId
from app.utils.image_utils import delete_image
from app.utils.image_utils import save_image
from pathlib import Path
import json
import logging
import time

logger = logging.getLogger("main")


class UserService:
    def __init__(self, user_repository: UserRepository):
        """
        Initialize the UserService with a UserRepository instance.
        :param user_repository: Repository to handle user database operations.
        """
        self.user_repository = user_repository

    def create_user(self, user_request: UserRequest, file_byte_array: Optional[bytearray]) -> dict:
        image_url = ''
        user_code = GenerateCodeForId.generate_random_code(6)
        if file_byte_array:
            logger.info("User has profile photo, will ensure create img flow!")
            image_url = f"{user_code}_{user_request.username}"
            filename = image_url
            directory = Path(__file__).resolve().parent.parent.parent / UPLOAD_DIR
            save_image(file_byte_array, filename, directory)

        user_request.code = user_code
        user = self.create_user_call_db(user_request, image_url)
        user_json = json.loads(UserMapper.to_user_response(user).model_dump_json())
        token = PasswordUtils.generate_hashed_token(user)
        response_payload = {
            **user_json,
            'token': token
        }

        return response_payload

    def reverify_user_and_generate_token(self, user_payload: dict) -> str:
        username = user_payload['username']
        user = self.get_user_by_user_name(username)

        is_pass_verified = PasswordUtils.verify_password(user_payload['password'], user.password)
        if not is_pass_verified:
            logger.error('Tried regenerating password, password does not match in req and db!')
            raise UserExceptionError('Password does not match, cannot regenerate token!')

        return PasswordUtils.generate_hashed_token(user)

    def create_user_call_db(self, user_request: UserRequest, image_url:Optional[str]) -> UserResponse:
        """
        Create a new user.
        :param image_url: Image url location to be stored if user inputs image
        :param user_request: UserRequest object with user details.
        :return: UserResponse object of the newly created user.
        """
        user = UserMapper.to_user(user_request, image_url)

        # User validation will go here!

        created_user = self.user_repository.create_user(user)
        return UserMapper.to_user_response(created_user)

    def get_user_by_user_code(self, code: str) -> UserResponse:
        """
        Retrieve a user by their ID.
        :param code: The code of the user.
        :return: UserResponse object if found.
        :raises UserNotFoundException: If the user is not found.
        """
        user = self.user_repository.get_user_by_code(code)
        if not user:
            raise UserExceptionError(f"User with usercode {code} not found")
        return UserMapper.to_user_response(user)

    def get_user_by_user_name(self, user_name: str) -> UserResponse:
        """
        NOTE: THIS METHOD RETURNS USER HASHED PASSWORD. USE WITH CAUTION
        Retrieve a user by their ID.
        :param user_name: The ID of the user.
        :return: UserResponse object if found.
        :raises UserNotFoundException: If the user is not found.
        """
        user = self.user_repository.get_user_by_user_name(user_name)
        if not user:
            raise UserExceptionError(f"User with username {user_name} not found")
        return UserMapper.to_user_response(user, True)

    def update_user(self, request: str, image_bytes: Optional[bytes]) -> UserResponse:
        try:
            request = UserRequest.parse_raw(request)
        except Exception as e:
            raise ResponseException("Unable to parse request", 422, e)

        if not request.code:
            raise ResponseException("User code is empty", 417)

        user = self.user_repository.get_user_by_code(request.code)
        if not user:
            raise ResponseException(f"User with code {user.code} not found", 404)

        image_uri = save_image(image_bytes, user.code, f"{UPLOAD_DIR}/user")

        user.name = request.name
        user.about = request.about
        user.color = request.color
        user.image_uri = image_uri
        user.updated_at = round(time.time() * 1000)
        user.updated_by = user.username

        self.user_repository.update_user(user)
        return UserMapper.to_user_response(user)

    def delete_user(self, code: str) -> dict:
        """
        Delete a user by their ID.
        :param code: The ID of the user to delete.
        :return: True if the user was successfully deleted.
        :raises UserNotFoundException: If the user is not found.
        """
        user = self.user_repository.get_user_by_code(code)
        if not user:
            raise UserExceptionError(f"User with ID {code} not found", "user_code")

        is_user_deleted = self.user_repository.delete_user(code)

        if is_user_deleted:
            logger.info('User deleted will try to delete profile photo!')

            delete_image(f"{user.code}_{user.username}.jpg")

        return {'is_user_deleted':is_user_deleted}

    def get_all_users(self) -> List[UserResponse]:
        """
        Retrieve all users.
        :return: List of UserResponse objects.
        """
        users = self.user_repository.get_all_users()
        return [UserMapper.to_user_response(user) for user in users]

