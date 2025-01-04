from app.exceptions.tokenException import TokenException
from app.services.userService import UserService
from app.utils.passwordUtils import PasswordUtils
from app.utils.operationHandler import handle_operation
from app.models.database import get_box
from app.repository.userRepository import UserRepository
from fastapi import APIRouter, HTTPException, status, Depends
from objectbox import Box
import json
import logging

logger = logging.getLogger('main')

router = APIRouter(
    prefix="/api/v1/token",
    tags=["Token"]
)

def get_user_service(box: Box = Depends(get_box)) -> UserService:
    user_repository = UserRepository(box=box)
    return UserService(user_repository)

@router.post("/regenerate-token", status_code=status.HTTP_200_OK)
async def regenerate_token_on_demand(
    encry_str: str,
    user_service: UserService = Depends(get_user_service)
):
    """
    Regenerate token on demand.
    """
    try:
        user_payload = json.loads(PasswordUtils.decrypt_aes_encoded_text(encry_str))
        regenerated_token = user_service.reverify_user_and_generate_token(user_payload)
        response_payload = {"token": regenerated_token}
        return handle_operation(response_payload)
    except TokenException as e:
        logger.error(f"User Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong re-generating token!"
        )
