from app.models.chat import Chat
from objectbox import Box
from typing import Optional

class ChatRepository:
    def __init__(self, box: Box):
        self.box = box
    def create(self, chat_data:Chat) -> Chat:
        """Create a new chat"""
        self.box.put(chat_data)
        return chat_data

    def get_by_code(self, code:str) -> Optional[Chat]:
        """
        Queries the db via chat response
        :return: ChatModel
        """
        db_query = self.box.query(Chat.code.equals(code)).build()
        assistants = db_query.find()
        return assistants[0] if assistants else None

    def delete_chat(self, code:str) -> bool:
        chat = self.get_by_code(code)
        if chat:
            self.box.remove(chat)  # Remove the chat entity
            return True

        return False