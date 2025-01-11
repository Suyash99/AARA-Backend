from app.dto.request.message_request import MessageRequest
from app.dto.response.server_response import ServerResponse
from app.repository.chat_repository import ChatRepository
from app.repository.user_repository import UserRepository
from app.services.assistant_service import AssistantService
from app.repository.assistant_repository import AssistantRepository
from app.models.database import get_box
from fastapi import APIRouter, File, UploadFile, Form, Depends, Request
from typing import  Optional
from functools import partial
from objectbox import Box

from app.utils.constants import APP_ID, API_VERSION
from app.utils.operation_handler import handle_operation
import logging

logger = logging.getLogger('main')

router = APIRouter(
    prefix=f"/{APP_ID}/{API_VERSION}/assistant",
    tags=["Assistant"],
)

# Injecting box from route
def get_service(box: Box = Depends(get_box)) -> AssistantService:
    assistant_repository = AssistantRepository(box=box)
    user_repository = UserRepository(box)
    chat_repository = ChatRepository(box)
    return AssistantService(assistant_repository,user_repository,chat_repository)

@router.post("/create", response_model=ServerResponse)
async def create_assistant(
    assistantRequest: str = Form(...),
    image: Optional[UploadFile] = File(None),
    assistant_service: AssistantService = Depends(get_service),
):
    """
    Creates a new assistant!
    """
    file_byte_array = bytearray(await image.read()) if image else None
    return handle_operation(partial(assistant_service.create_assistant,assistantRequest,file_byte_array))

@router.get("/voice-models")
def get_voice_models(assistant_service: AssistantService = Depends(get_service)):
    """
    Retrieve list of voice models
    """
    return handle_operation(partial(assistant_service.list_assistant_voice_models))

@router.post("/response")
def get_assistant_response(messageRequest:MessageRequest,request:Request,assistant_service: AssistantService = Depends(get_service)):
    """
    Retrieve response from assistant.
    """
    return handle_operation(partial(assistant_service.generate_response, messageRequest, request))

@router.delete("/delete/{code}")
def delete_assistant(code:str, assistant_service: AssistantService = Depends(get_service)):
    """
    Delete assistant via assistant_code
    """
    return handle_operation(partial(assistant_service.delete_assistant, code))