from app.services.userService import UserService
from app.mapper.userRequest import UserRequest
from app.models.database import get_box
from app.exceptions.userException import UserExceptionError
from app.repository.userRepository import UserRepository
from objectbox import Box
from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form, Depends
from typing import  Optional
from pydantic import EmailStr
from app.utils.operationHandler import handle_operation
import logging

logger = logging.getLogger('main')

router = APIRouter(
    prefix="/api/v1/user",
    tags=["Users"]
)

def get_user_service(box: Box = Depends(get_box)) -> UserService:
    user_repository = UserRepository(box=box)
    return UserService(user_repository)

@router.post("/", status_code=status.HTTP_200_OK)
async def create_user(
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    colour_code: str = Form(...),
    user_photo: Optional[UploadFile] = File(None),
    user_service: UserService = Depends(get_user_service),
):
    """
    Create a new user.
    """
    try:
        # Construct user request
        user_request = UserRequest(
            username=username,
            user_code='',
            email=email,
            password=password,
            user_photo_bytes='',
            colour_code=colour_code,
            created_at=None,
            updated_at=None
        )

        # Read file if provided
        file_byte_array = bytearray(await user_photo.read()) if user_photo else None

        # Call user service
        response = user_service.create_user(user_request, file_byte_array)

        # Construct payload
        response_payload = {"token": response}
        return handle_operation(response_payload)

    except UserExceptionError as e:
        logger.error(f"User Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User creation failed: {str(e)}"
        )


@router.get("/{user_code}")
def get_user(user_code: str, user_service: UserService = Depends(get_user_service)):
    """
    Retrieve a user by ID.
    """
    user = user_service.get_user_by_user_code(user_code)
    return handle_operation(user)

@router.get("/")
def get_all_users(user_service: UserService = Depends(get_user_service)):
    """
    Retrieve all users.
    """
    user = user_service.get_all_users()
    return handle_operation(user)

@router.put("/{user_code}")
def update_user(user_code: str, user_request: UserRequest, user_service: UserService = Depends(get_user_service)):
    """
    Update an existing user.
    """
    user = user_service.update_user(user_code, user_request)
    return handle_operation(user)

@router.delete("/{user_code}")
def delete_user(user_code: str, user_service: UserService = Depends(get_user_service)):
    """
    Delete a user by user_code.
    """
    is_user_deleted = user_service.delete_user(user_code)
    response_payload = {'user_deleted':is_user_deleted}
    return handle_operation(response_payload)
