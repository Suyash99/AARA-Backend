from app.mapper.serverResponseMapper import ServerResponse
from app.services.user_service import UserService
from app.mapper.user_request import UserRequest
from app.models.database import get_box
from app.mapper.tokenRequest import RegenerateTokenRequest
from app.exceptions.tokenException import TokenException
from app.utils.crypto_utils import PasswordUtils
from app.utils.constants import UPLOAD_DIR
from app.exceptions.userException import UserExceptionError
from app.repository.userRepository import UserRepository
from fastapi.responses import Response
from requests_toolbelt import MultipartEncoder
from objectbox import Box
from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form, Depends
from typing import  Optional
from functools import partial
from pathlib import Path
import json

from app.utils.constants import APP_ID, API_VERSION
from app.utils.operation_handler import handle_operation
import logging

logger = logging.getLogger('main')

router = APIRouter(
    prefix=f"/{APP_ID}/{API_VERSION}/user",
    tags=["Users"],
)

def get_service(box: Box = Depends(get_box)) -> UserService:
    user_repository = UserRepository(box=box)
    return UserService(user_repository)

@router.post("/", status_code=status.HTTP_200_OK)
async def create(
    name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    color: str = Form(...),
    about: str = Form(...),
    user_photo: Optional[UploadFile] = File(None),
    user_service: UserService = Depends(get_service),
):
    """
    Create a new user.
    """
    try:
        # Construct user request
        user_request = UserRequest(
            name = name,
            username=username,
            code='',
            password=password,
            color=color,
            about=about
        )

        # Read file if provided
        file_byte_array = bytearray(await user_photo.read()) if user_photo else None

        response_payload = user_service.create_user(user_request, file_byte_array)
        mfd_fields = {
            'userBody': json.dumps(response_payload)
        }

        if file_byte_array:
            #Image will be in-format f{code}_{username}
            image_name = f"{response_payload['code']}_{username}.jpg"
            full_image_path = Path(__file__).resolve().parent.parent.parent / UPLOAD_DIR / image_name
            mfd_fields['userImage'] =  (image_name, open(full_image_path, 'rb'), 'image/jpeg')

        mfd = MultipartEncoder(fields=mfd_fields)

        return Response(mfd.to_string(), media_type=mfd.content_type)

    except UserExceptionError as e:
        logger.error(f"User Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User creation failed: {str(e)}"
        )


@router.get("/{code}")
def get(code: str, user_service: UserService = Depends(get_service)):
    """
    Retrieve a user by ID.
    """
    return handle_operation(partial(user_service.get_user_by_user_code,code))

@router.get("/")
def get_all(user_service: UserService = Depends(get_service)):
    """
    Retrieve all users.
    """
    return handle_operation(user_service.get_all_users)

@router.put(path="/")
async def update(
        userBody: str = Form(...),
        userImage: Optional[UploadFile] = File(None),
        service: UserService = Depends(get_service)):
    """
    Update an existing user.
    """
    image_bytes = bytearray(await userImage.read()) if userImage else None
    return handle_operation(partial(service.update_user, userBody, image_bytes))

@router.delete("/{code}")
def delete(code: str, user_service: UserService = Depends(get_service)):
    """
    Delete a user by user_code.
    """
    return handle_operation(partial(user_service.delete_user, code))

@router.put("/re-login", status_code=status.HTTP_200_OK)
def token_regen(
        request: RegenerateTokenRequest,
        user_service: UserService = Depends(get_service)
):
    """
    Regenerate token on demand.
    """
    return handle_operation(partial(user_service.regenerate_token_on_demand,request.username,request.password))
