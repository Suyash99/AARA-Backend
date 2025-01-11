from app.exceptions.assistant_exception import AssistantExceptionError
from app.exceptions.auth_exception import AuthException
from app.repository.assistant_repository import AssistantRepository
from app.dto.request.assistant_request import AssistantRequest
from app.dto.response.assistant_response import AssistantResponse
from app.dto.request.message_request import MessageRequest
from app.mapper.assistant_mapper import AssistantMapper
from app.repository.chat_repository import ChatRepository
from app.repository.user_repository import UserRepository
from app.services.gemini_service import GeminiService
from app.utils.crypto_utils import PasswordUtils
from app.utils.generate_code_for_id import GenerateCodeForId
from app.utils.image_utils import save_image
from app.utils.load_assistant_assets import generate_assistant_response
from app.utils.constants import RVC_MODEL_MAP, UPLOAD_DIR, ASSISTANT_FOLDER
from fastapi import Request
from typing import Optional
import logging

logger = logging.getLogger('main')

class AssistantService:
    def __init__(self,
                 assistant_repository: AssistantRepository,
                 user_repository: UserRepository,
                 chat_repository: ChatRepository
                 ):
        """
        Initialize the AssistantService with a AssistantRepository instance.
        :param assistant_repository: Repository to handle assistant database operations.
        """
        self.assistant_repository = assistant_repository
        self.user_repository = user_repository
        self.chat_repository = chat_repository

    def create_assistant(self, request: str, file_byte_array: Optional[bytearray]) -> AssistantResponse:
        try:
            assistant_request = AssistantRequest.parse_raw(request)
        except Exception as e:
            raise Exception("Error converting to incoming assistant request payload to json!")

        code = GenerateCodeForId.generate_random_code(6)

        #Check if already created
        if self.assistant_repository.get_by_code(code):
            raise AssistantExceptionError(f"Assistant already created with code {code}", "code")

        image_uri = ''
        if file_byte_array:
            logger.info("Assistant has photo attached, will ensure create img flow!")
            image_uri = f"{code}_{assistant_request.name}"
            filename = image_uri
            directory = UPLOAD_DIR / ASSISTANT_FOLDER
            save_image(file_byte_array, filename, directory)

        assistant_request.code = code
        assistant_request.imageUri = image_uri
        assistant = self.assistant_repository.create(assistant_request)
        return AssistantMapper.to_assistant_response(assistant)

    def list_assistant_voice_models(self) -> list:
        return RVC_MODEL_MAP.keys()

    def generate_response(self, message_request: MessageRequest, request: Request):
        token = request.headers.get('Authorization')

        token_payload = PasswordUtils.verify_hashed_token(token)

        if not token_payload['code']:
            raise AuthException('Token does not contain required field/s!', 401)

        #Get gemini key from user model
        user = self.user_repository.get_user_by_code(token_payload['code'])

        gemini_api_key = user.gemini_api_key

        message_content = message_request.content

        chat = self.chat_repository.get_by_code(message_request.chatCode)
        assistant = self.assistant_repository.get_by_id(chat.assistant_id)

        return GeminiService.generate_content(message_content,assistant.systemPrompt,gemini_api_key,assistant.temperature)

    def delete_assistant(self, code:str) -> dict:
        assistant = self.assistant_repository.get_by_code(code)

        if not assistant:
            raise AssistantExceptionError(f"Assistant not found with code: {code}", "code")

        assistant_delete_status = self.assistant_repository.delete_assistant(code)

        return {'assistant_delete_status': assistant_delete_status}