from app.exceptions.assistant_exception import AssistantExceptionError
from app.repository.assistant_repository import AssistantRepository
from app.dto.request.assistant_request import AssistantRequest
from app.dto.response.assistant_response import AssistantResponse
from app.mapper.assistant_mapper import AssistantMapper
from app.utils.generate_code_for_id import GenerateCodeForId
from app.utils.image_utils import save_image
from app.utils.load_assistant_assets import generate_assistant_response
from app.utils.constants import MODEL_MAP, UPLOAD_DIR, ASSISTANT_FOLDER

from typing import Optional
import logging

logger = logging.getLogger('main')

class AssistantService:
    def __init__(self, assistant_repository: AssistantRepository):
        """
        Initialize the AssistantService with a AssistantRepository instance.
        :param assistant_repository: Repository to handle assistant database operations.
        """
        self.assistant_repository = assistant_repository

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
        return MODEL_MAP.keys()

    def run_assistant_response(self, assistant_name: str):
        return generate_assistant_response(assistant_name)

    def delete_assistant(self, code:str) -> dict:
        assistant = self.assistant_repository.get_by_code(code)

        if not assistant:
            raise AssistantExceptionError(f"Assistant not found with code: {code}", "code")

        assistant_delete_status = self.assistant_repository.delete_assistant(code)

        return {'assistant_delete_status': assistant_delete_status}