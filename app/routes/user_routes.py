from app.services.user_service import UserService
from app.dto.request.user_request import UserRequest
from app.models.database import get_box
from app.dto.request.auth_request import RegenerateAuthRequest
from app.exceptions.user_exception import UserExceptionError
from app.repository.user_repository import UserRepository
from objectbox import Box
from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form, Depends
from typing import  Optional
from functools import partial

from app.utils.constants import APP_ID, API_VERSION
from app.utils.operation_handler import handle_operation
import logging

logger = logging.getLogger('main')

router_user = APIRouter(
    prefix=f"/{APP_ID}/{API_VERSION}/user",
    tags=["Users"],
)

def get_service(box: Box = Depends(get_box)) -> UserService:
    user_repository = UserRepository(box=box)
    return UserService(user_repository)

@router_user.post("/", status_code=status.HTTP_200_OK)
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

        return handle_operation(partial(user_service.create_user,user_request, file_byte_array))

    except UserExceptionError as e:
        logger.error(f"User Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User creation failed: {str(e)}"
        )

@router_user.get("/image/{code}")
def get_image_by_user_code(code:str, user_service: UserService = Depends(get_service)):
    """
    Retrieves an image of user from server

    """
    return user_service.get_image_from_user_code(code)

@router_user.get("/{code}")
def get(code: str, user_service: UserService = Depends(get_service)):
    """
    Retrieve a user by ID.
    """
    return handle_operation(partial(user_service.get_user_by_user_code,code))

@router_user.get("/")
def get_all(user_service: UserService = Depends(get_service)):
    """
    Retrieve all users.
    """
    return handle_operation(user_service.get_all_users)

@router_user.put(path="/")
async def update(
        userBody: str = Form(...),
        userImage: Optional[UploadFile] = File(None),
        service: UserService = Depends(get_service)):
    """
    Update an existing user.
    """
    image_bytes = bytearray(await userImage.read()) if userImage else None
    return handle_operation(partial(service.update_user, userBody, image_bytes))

@router_user.delete("/{code}")
def delete(code: str, user_service: UserService = Depends(get_service)):
    """
    Delete a user by user_code.
    """
    return handle_operation(partial(user_service.delete_user, code))

@NotImplemented
@router_user.put("/re-login", status_code=status.HTTP_200_OK)
def token_regen(
        request: RegenerateAuthRequest,
        user_service: UserService = Depends(get_service)
):
    """
    Regenerate token on demand.
    """
    return handle_operation(partial(user_service.regenerate_token_on_demand,request.username,request.password))
