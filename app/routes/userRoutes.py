from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.services.userService import UserService
from app.mapper.userRequest import UserRequest
from app.mapper.userResponse import UserResponse
from app.exceptions.userException import UserExceptionError

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
def create_user(user_request: UserRequest, user_service: UserService):
    """
    Create a new user.
    """
    try:
        return user_service.create_user_and_generate_hashed_token(user_request)
    except UserExceptionError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, user_service: UserService ):
    """
    Retrieve a user by ID.
    """
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
def get_all_users(user_service: UserService = Depends(get_user_service)):
    """
    Retrieve all users.
    """
    return user_service.get_all_users()

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_request: UserRequest, user_service: UserService = Depends(get_user_service)):
    """
    Update an existing user.
    """
    try:
        return user_service.update_user(user_id, user_request)
    except UserExceptionError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """
    Delete a user by ID.
    """
    if user_service.delete_user(user_id):
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
