from functools import partial

from app.dto.request.user_request import UserRequest
from app.services.user_service import UserService
from app.repository.user_repository import UserRepository
from app.utils.constants import UPLOAD_DIR, USER_FOLDER
from app.exceptions.auth_exception import AuthException
from requests_toolbelt import MultipartEncoder
from fastapi.responses import Response
from fastapi import HTTPException, status
from typing import Optional
from pathlib import Path
import json
import logging

from app.utils.operation_handler import handle_operation

logger = logging.getLogger('main')

class AuthService:
    def __init__(self, user_repository: UserRepository,user_service: UserService):
        """
        Initialize the UserService with a UserRepository instance.
        :param user_repository: Repository to handle user database operations.
        """
        self.user_repository = user_repository
        self.user_service = user_service

    def user_sign_up(self, incoming_user_request: dict, user_image: Optional[bytearray]):
        # Construct user request
        name = incoming_user_request['name']
        username = incoming_user_request['username']
        password = incoming_user_request['password']
        color = incoming_user_request['color']
        about = incoming_user_request['about']
        user_request = UserRequest(
            name=name,
            username=username,
            code='',
            password=password,
            color=color,
            about=about
        )

        return handle_operation(partial(self.user_service.create_user, user_request, user_image))

    def user_sign_in(self, user_payload: dict):
        return UserService.reverify_user_and_generate_token(self.user_service,user_payload)