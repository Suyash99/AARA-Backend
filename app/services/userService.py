from typing import List
from app.exceptions.userException import UserExceptionError
from app.mapper.userMapper import UserMapper
from app.mapper.userResponse import UserResponse
from app.mapper.userRequest import UserRequest
from app.repository.userRepository import UserRepository
from app.utils.passwordUtils import PasswordUtils

class UserService:
    def __init__(self, user_repository: UserRepository):
        """
        Initialize the UserService with a UserRepository instance.
        :param user_repository: Repository to handle user database operations.
        """
        self.user_repository = user_repository

    def create_user_and_generate_hashed_token(self, user_request: UserRequest) -> str:
        user = self.create_user(user_request)
        return PasswordUtils.generate_hashed_token(user)

    def create_user(self, user_request: UserRequest) -> UserResponse:
        """
        Create a new user.
        :param user_request: UserRequest object with user details.
        :return: UserResponse object of the newly created user.
        """
        user = UserMapper.to_user(user_request)
        created_user = self.user_repository.create_user(user)
        return UserMapper.to_user_response(created_user).model_validate(created_user)

    def get_user_by_id(self, user_code: str) -> UserResponse:
        """
        Retrieve a user by their ID.
        :param user_id: The ID of the user.
        :return: UserResponse object if found.
        :raises UserNotFoundException: If the user is not found.
        """
        user = self.user_repository.get_user_by_user_code(user_code)
        if not user:
            raise UserExceptionError(f"User with ID {user_code} not found")
        return UserResponse.from_orm(user)

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

    def update_user(self, user_id: int, user_request: UserRequest) -> UserResponse:
        """
        Update an existing user's details.
        :param user_id: The ID of the user to update.
        :param user_request: UserRequest object with updated details.
        :return: UserResponse object of the updated user.
        :raises UserNotFoundException: If the user is not found.
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserExceptionError(f"User with ID {user_id} not found", "")

        user.username = user_request.username
        user.email = user_request.email
        user.password = user_request.password
        user.user_code = user_request.user_code
        user.colour_code = user_request.colour_code
        user.updated_at = user_request.updated_at

        self.user_repository.update_user(user)
        return UserResponse.from_orm(user)

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by their ID.
        :param user_id: The ID of the user to delete.
        :return: True if the user was successfully deleted.
        :raises UserNotFoundException: If the user is not found.
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserExceptionError(f"User with ID {user_id} not found", "")
        return self.user_repository.delete_user(user_id)

    def get_all_users(self) -> List[UserResponse]:
        """
        Retrieve all users.
        :return: List of UserResponse objects.
        """
        users = self.user_repository.get_all_users()
        return [UserResponse.from_orm(user) for user in users]

    def count_users(self) -> int:
        """
        Count the total number of users.
        :return: The count of users.
        """
        return self.user_repository.count_users()

