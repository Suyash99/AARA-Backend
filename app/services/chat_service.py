from app.repository.chat_repository import ChatRepository
from app.dto.response.chat_response import ChatResponse
from app.mapper.chat_mapper import ChatMapper
import logging

logger = logging.getLogger("main")

class ChatService:
    def __init__(self, chat_repository: ChatRepository):
        """
        Initialize the UserService with a UserRepository instance.
        :param chat_repository: Repository to handle user database operations.
        """
        self.chat_repository = chat_repository

    def get_chat_by_chat_code(self, code:str) -> ChatResponse:
        chat= self.chat_repository.get_by_code(code)

        if not chat:
            raise Exception(f"Chat not found with code- {code}")

        return ChatMapper.to_chat_response(chat)