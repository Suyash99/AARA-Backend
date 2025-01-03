from app.models import User
from objectbox import Box, query
from typing import Optional, List

class UserRepository:
    def __init__(self, box: Box):
        self.box = box

    def create_user(self, user_data: User) -> User:
        """Create a new user."""
        return self.box.put(user_data)

    def get_user_by_user_code(self, user_code: str) -> Optional[User]:
        """Retrieve a user by ID."""
        db_query = self.query_in_db("user_code = ?", [user_code]).build()
        users = db_query.find()
        return users[0] if users else None

    def get_user_by_id(self, id: int) -> Optional[User]:
        """Retrieve a user by ID."""
        return self.box.get(id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email."""
        db_query = self.query_in_db("email = ?", [email]).build()
        users = db_query.find()
        return users[0] if users else None

    def update_user(self, user_code: str) -> bool:
        """Update a user's details."""
        db_query = self.query_in_db("user_code = ?", [user_code]).build()
        user = db_query.find()
        return self.box.put(user) is not None

    def delete_user(self, user_code: str) -> bool:
        """Delete a user."""
        return self.box.remove(user_code)

    def query_in_db(self, field_names:str, field_values:List[str]) -> query:
        return self.box.query(field_names, field_values)

    def get_all_users(self) -> List[User]:
        """
        Fetch all users using the repository.
        :return: List of User entities.
        """
        return self.box.get_all()
