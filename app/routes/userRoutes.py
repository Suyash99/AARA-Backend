from app.services.userService import UserService
from app.mapper.userRequest import UserRequest
from app.exceptions.userException import UserExceptionError
from app.repository.userRepository import UserRepository
from app.mapper.serverResponseMapper import ServerResponse
from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form, Depends
from typing import  Optional
from pydantic import EmailStr
from app.utils.operationHandler import handle_operation
import logging

logger = logging.getLogger('main')

router = APIRouter(
    prefix="/api/v1/token",
    tags=["Token"]
)

@router.post("/", response_model=ServerResponse, status_code=status.HTTP_200_OK)
async def create_user(
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    colour_code: str = Form(...),
    file: Optional[UploadFile] = File(None),
    user_service: UserService = Depends(UserService(UserRepository())),
    ):
    """
    Create a new user.
    """
    try:
        user_request = UserRequest(
            username=username,
            user_code='',
            email=email,
            password=password,
            user_photo_bytes=None,
            colour_code=colour_code
        )
        file_byte_array = bytearray(await file.read()) if file else None
        response = user_service.create_user(user_request,file_byte_array)
        response_payload = {'token':response}
        return handle_operation(response_payload)
    except UserExceptionError as e:
        logger.error(f'User Exception- {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong!! Problem is not with you, its us :(')

@router.get("/{user_code}", response_model=ServerResponse)
def get_user(user_code: str, user_service: UserService ):
    """
    Retrieve a user by ID.
    """
    user = user_service.get_user_by_user_code(user_code)
    return handle_operation(user)

@router.get("/", response_model=ServerResponse)
def get_all_users(user_service: UserService):
    """
    Retrieve all users.
    """
    user = user_service.get_all_users()
    return handle_operation(user)

@router.put("/{user_code}", response_model=ServerResponse)
def update_user(user_code: str, user_request: UserRequest, user_service: UserService):
    """
    Update an existing user.
    """
    user = user_service.update_user(user_code, user_request)
    return handle_operation(user)

@router.delete("/{user_code}", response_model=ServerResponse)
def delete_user(user_code: str, user_service: UserService):
    """
    Delete a user by user_code.
    """
    is_user_deleted = user_service.delete_user(user_code)
    response_payload = {'user_deleted':is_user_deleted}
    return handle_operation(response_payload)
