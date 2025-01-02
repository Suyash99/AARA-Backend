from app.services.userService import UserService
from app.mapper.userRequest import UserRequest
from app.mapper.userResponse import UserResponse
from app.exceptions.userException import UserExceptionError
from app.repository.userRepository import UserRepository
from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form, Depends
from typing import List, Optional
from pydantic import EmailStr

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
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
            email=email,
            password=password,
            colour_code=colour_code
        )
        file_byte_array = bytearray(await file.read()) if file else None
        return user_service.create_user(user_request,file_byte_array)
    except UserExceptionError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{user_code}", response_model=UserResponse)
def get_user(user_code: str, user_service: UserService ):
    """
    Retrieve a user by ID.
    """
    user = user_service.get_user_by_id(user_code)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
def get_all_users(user_service: UserService):
    """
    Retrieve all users.
    """
    return user_service.get_all_users()

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_request: UserRequest, user_service: UserService):
    """
    Update an existing user.
    """
    try:
        return user_service.update_user(user_id, user_request)
    except UserExceptionError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, user_service: UserService):
    """
    Delete a user by ID.
    """
    if user_service.delete_user(user_id):
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
