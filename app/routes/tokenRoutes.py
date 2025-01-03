from app.exceptions.tokenException import TokenException
from app.services.userService import UserService
from app.utils.passwordUtils import PasswordUtils
from app.mapper.serverResponseMapper import ServerResponse
from fastapi import APIRouter, HTTPException, status
from app.utils.operationHandler import handle_operation
import json
import logging

logger = logging.getLogger('main')

router = APIRouter(
    prefix="/api/v1/token",
    tags=["Token"]
)

@router.post("/regenerate-token", response_model=ServerResponse, status_code=status.HTTP_200_OK)
async def regenerate_token_on_demand(encry_str:str, user_service:UserService):
    """
    Create a new user.
    """
    try:
        user_payload = json.loads(PasswordUtils.decrypt_aes_encoded_text(encry_str))
        regenerated_token = user_service.reverify_user_and_generate_token(user_payload)
        response_payload = {'token':regenerated_token}
        return handle_operation(response_payload)
    except TokenException as e:
        logger.error(f'User Exception- {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong re-generating token!')