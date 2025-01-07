from app.models.assistant import Assistant
from app.dto.response.assistant_response import AssistantResponse
from objectbox import Box, query
from typing import Optional, List


class AssistantRepository:
    def __init__(self, box: Box):
        self.box = box
    def create(self, assistant_data:Assistant) -> Assistant:
        """Create a new user."""
        self.box.put(assistant_data)
        return assistant_data

    def get_by_code(self, code:str) -> Optional[Assistant]:
        """
        Queries the db via assistant response
        :return: AssistantResponse
        """
        db_query = self.box.query(Assistant.code.equals(code)).build()
        users = db_query.find()
        return users[0] if users else None