from app.services.auth_service import AuthService
from app.models.database import get_box
from app.dto.request.auth_request import RegenerateAuthRequest
from app.repository.user_repository import UserRepository
from app.services.user_service import UserService
from objectbox import Box
from fastapi import APIRouter, status, File, UploadFile, Form, Depends
from typing import Optional
from functools import partial

from app.utils.constants import APP_ID, API_VERSION
from app.utils.operation_handler import handle_operation
import logging

logger = logging.getLogger('main')

router_auth = APIRouter(
    prefix=f"/{APP_ID}/{API_VERSION}/auth",
    tags=["Auth"],
)


def get_service(box: Box = Depends(get_box)) -> AuthService:
    user_repository = UserRepository(box=box)
    user_service = UserService(user_repository)
    return AuthService(user_repository,user_service)


@router_auth.post("/sign-up", status_code=status.HTTP_200_OK)
async def sign_up_user(
        name: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        color: str = Form(...),
        about: str = Form(...),
        user_photo: Optional[UploadFile] = File(None),
        auth_service: AuthService = Depends(get_service),
):
    """
    Create a new user.
    """
    # Read file if provided
    file_byte_array = bytearray(await user_photo.read()) if user_photo else None
    incoming_request = {
        'name': name,
        'username': username,
        'password': password,
        'color': color,
        'code': '',
        'about': about,
    }
    return auth_service.user_sign_up(incoming_request, file_byte_array)


@router_auth.put("/sign-in", status_code=status.HTTP_200_OK)
def user_sign_in(
        request: RegenerateAuthRequest,
        auth_service: AuthService = Depends(get_service)
):
    """
    Regenerate token on demand.
    """
    user_payload = {
        'username':request.username,
        'password':request.password
    }
    return handle_operation(partial(auth_service.user_sign_in, user_payload))
