from typing import List, Optional
import base64
from app.exceptions.userException import UserExceptionError
from app.mapper.userMapper import UserMapper
from app.mapper.userResponse import UserResponse
from app.mapper.userRequest import UserRequest
from app.repository.userRepository import UserRepository
from app.utils.passwordUtils import PasswordUtils
from app.utils.generateCodeForId import GenerateCodeForId
from app.utils.storeImageUtils import save_image
from app.validations.userValidation import UserValidation
import logging


logger = logging.getLogger("main")

class UserService:
    def __init__(self, user_repository: UserRepository):
        """
        Initialize the UserService with a UserRepository instance.
        :param user_repository: Repository to handle user database operations.
        """
        self.user_repository = user_repository

    def create_user(self, user_request: UserRequest, file_byte_array: Optional[bytearray]) -> str:
        profile_image_bytes = base64.b64encode(file_byte_array).decode('utf-8') if file_byte_array else ''
        user_code = GenerateCodeForId.generate_random_code(6)
        if file_byte_array:
            logger.info("User has profile photo, will ensure create img flow!")
            filename = f'{user_code}_{user_request.username}.jpg'
            save_image(filename, file_byte_array)

        user_request.user_photo_bytes = profile_image_bytes
        user_request.user_code = user_code
        user = self.create_user_call_db(user_request)
        return PasswordUtils.generate_hashed_token(user)

    def reverify_user_and_generate_token(self,user_payload:dict) -> str:
        user_code = user_payload['user_code']
        user = self.get_user_by_user_code(user_code)

        is_pass_verified = PasswordUtils.verify_password(user_payload['password'],user.password)

        if not is_pass_verified:
            logger.error('Tried regenerating password, password does not match in req and db!')
            raise UserExceptionError('Password does not match!')

        return PasswordUtils.generate_hashed_token(user)

    def create_user_call_db(self, user_request: UserRequest) -> UserResponse:
        """
        Create a new user.
        :param user_request: UserRequest object with user details.
        :return: UserResponse object of the newly created user.
        """
        user = UserMapper.to_user(user_request)

        #User validation will go here!



        created_user = self.user_repository.create_user(user)
        return UserMapper.to_user_response(created_user)

    def get_user_by_user_code(self, user_code: str) -> UserResponse:
        """
        Retrieve a user by their ID.
        :param user_code: The ID of the user.
        :return: UserResponse object if found.
        :raises UserNotFoundException: If the user is not found.
        """
        user = self.user_repository.get_user_by_user_code(user_code)
        if not user:
            raise UserExceptionError(f"User with ID {user_code} not found")
        return UserResponse.model_validate(user)

    def get_user_by_email(self, email: str) -> UserResponse:
        """
        Retrieve a user by their email.
        :param email: The email of the user.
        :return: UserResponse object if found.
        :raises UserNotFoundException: If the user is not found.
        """
        user = self.user_repository.get_user_by_email(email)
        if not user:
            raise UserExceptionError(f"User with email {email} not found", "email")
        return UserResponse.model_validate(user)

    def update_user(self, user_code: str, user_request: UserRequest) -> UserResponse:
        """
        Update an existing user's details.
        :param user_code: The user_code of the user to update.
        :param user_request: UserRequest object with updated details.
        :return: UserResponse object of the updated user.
        :raises UserNotFoundException: If the user is not found.
        """
        user = self.user_repository.get_user_by_user_code(user_code)
        if not user:
            raise UserExceptionError(f"User with ID {user_code} not found", "user_code")

        user.username = user_request.username
        user.email = user_request.email
        user.user_code = user_request.user_code
        user.colour_code = user_request.colour_code
        user.updated_at = None

        self.user_repository.update_user(user)
        return UserResponse.model_validate(user)

    def delete_user(self, user_code: str) -> bool:
        """
        Delete a user by their ID.
        :param user_code: The ID of the user to delete.
        :return: True if the user was successfully deleted.
        :raises UserNotFoundException: If the user is not found.
        """
        user = self.user_repository.get_user_by_user_code(user_code)
        if not user:
            raise UserExceptionError(f"User with ID {user_code} not found", "user_code")
        return self.user_repository.delete_user(user_code)

    def get_all_users(self) -> List[UserResponse]:
        """
        Retrieve all users.
        :return: List of UserResponse objects.
        """
        users = self.user_repository.get_all_users()
        return [UserResponse.model_validate(user) for user in users]

