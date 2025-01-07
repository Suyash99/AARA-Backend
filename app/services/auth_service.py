from app.dto.request.user_request import UserRequest
from app.services.user_service import UserService
from app.repository.user_repository import UserRepository
from app.utils.constants import UPLOAD_DIR
from app.exceptions.auth_exception import AuthException
from requests_toolbelt import MultipartEncoder
from fastapi.responses import Response
from fastapi import HTTPException, status
from typing import Optional
from pathlib import Path
import json
import logging

logger = logging.getLogger('main')

class AuthService:
    def __init__(self, user_repository: UserRepository,user_service: UserService):
        """
        Initialize the UserService with a UserRepository instance.
        :param user_repository: Repository to handle user database operations.
        """
        self.user_repository = user_repository
        self.user_service = user_service

    def user_sign_up(self, incoming_user_request: dict, user_image: Optional[bytearray]) -> Response:
        try:
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

            response_payload = self.user_service.create_user(user_request,user_image)
            mfd_fields = {
                'userBody': json.dumps(response_payload)
            }

            if user_image:
                # Image will be in-format f{code}_{username}
                image_name = f"{response_payload['code']}_{username}.jpg"
                full_image_path = Path(__file__).resolve().parent.parent.parent / UPLOAD_DIR / image_name
                mfd_fields['userImage'] = (image_name, open(full_image_path, 'rb'), 'image/jpeg')

            mfd = MultipartEncoder(fields=mfd_fields)

            return Response(mfd.to_string(), media_type=mfd.content_type)

        except AuthException as e:
            logger.error(f"Auth Exception: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User creation failed: {str(e)}"
            )

    def user_sign_in(self, user_payload: dict):
        return UserService.reverify_user_and_generate_token(self.user_service,user_payload)