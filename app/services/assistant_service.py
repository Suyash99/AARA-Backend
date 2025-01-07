from app.exceptions.assistant_exception import AssistantExceptionError
from app.repository.assistant_repository import AssistantRepository
from app.dto.request.assistant_request import AssistantRequest
from app.mapper.assistant_mapper import AssistantMapper
from app.utils.generateCodeForId import GenerateCodeForId
from app.utils.image_utils import save_image
from typing import Optional
from pathlib import Path
from app.utils.constants import UPLOAD_DIR, ASSISTANT_FOLDER
import logging

logger = logging.getLogger('main')

class AssistantService:
    def __init__(self, assistant_repository: AssistantRepository):
        """
        Initialize the AssistantService with a AssistantRepository instance.
        :param assistant_repository: Repository to handle assistant database operations.
        """
        self.assistant_repository = assistant_repository

    def create_assistant(self, request: str, file_byte_array: Optional[bytearray]) -> dict:
        try:
            assistant_request = AssistantRequest.parse_raw(request)
        except Exception as e:
            raise Exception("Error converting to incoming assistant request payload to json!")

        code = GenerateCodeForId.generate_random_code(6)
        #Check if already created
        if self.assistant_repository.get_by_code(code):
            raise AssistantExceptionError

        image_uri = ''
        if file_byte_array:
            logger.info("Assistant has photo attached, will ensure create img flow!")
            image_uri = f"{code}_{assistant_request.name}"
            filename = image_uri
            directory = UPLOAD_DIR / ASSISTANT_FOLDER
            save_image(file_byte_array, filename, directory)

        assistant_request.code = code
        assistant_request.imageUri = image_uri
        self.assistant_repository.create(assistant_request)

        return {'assistant_code': code}