from functools import partial

from app.services.assistant_service import AssistantService
from app.services.user_service import UserService
from app.repository.assistant_repository import AssistantRepository
from app.dto.request.user_request import UserRequest
from app.models.database import get_box
from app.utils.constants import UPLOAD_DIR
from app.exceptions.user_exception import UserExceptionError
from fastapi.responses import Response
from requests_toolbelt import MultipartEncoder
from objectbox import Box
from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form, Depends
from typing import  Optional
from pathlib import Path
import json

from app.utils.constants import APP_ID, API_VERSION
from app.utils.operation_handler import handle_operation
import logging

logger = logging.getLogger('main')

router_assistant = APIRouter(
    prefix=f"/{APP_ID}/{API_VERSION}/assistant",
    tags=["Assistants"],
)

def get_service(box: Box = Depends(get_box)) -> AssistantService:
    assistant_repository = AssistantRepository(box=box)
    return AssistantService(assistant_repository)

@router_assistant.post("/create", status_code=status.HTTP_200_OK)
async def create(
    assistantRequest: str = Form(...),
    image: Optional[UploadFile] = File(None),
    assistant_service: AssistantService = Depends(get_service),
):
    """
    Creates a new assistant!
    """
    file_byte_array = bytearray(await image.read()) if image else None
    return handle_operation(partial(assistant_service.create_assistant,assistantRequest,file_byte_array))

@router_assistant.get("/voice-models")
def get():
    """
    Retrieve list of voice models
    """
    return

@router_assistant.post("/response")
def get_all(user_service: UserService = Depends(get_service)):
    """
    Retrieve response from assistant.
    """
    return handle_operation(user_service.get_all_users)

@router_assistant.delete(path="/delete/{assistant_code}")
async def update(assistant_code:str):
    """
        Delete assistant via assistant_code

    """
    return ''