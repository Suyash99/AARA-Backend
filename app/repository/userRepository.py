from app.models.user import User
from objectbox import Box, query
from typing import Optional, List

class UserRepository:
    def __init__(self, box: Box):
        self.box = box

    def create_user(self, user_data: User) -> User:
        """Create a new user."""
        self.box.put(user_data)
        return user_data

    def get_user_by_user_code(self, user_code: str) -> Optional[User]:
        """Retrieve a user by user_code."""
        db_query = self.box.query(User.user_code.equals(user_code)).build()
        users = db_query.find()
        return users[0] if users else None

    def get_user_by_user_name(self, user_name: str) -> Optional[User]:
        """Retrieve a user by user_code."""
        db_query = self.box.query(User.username.equals(user_name)).build()
        users = db_query.find()
        return users[0] if users else None

    def get_user_by_id(self, id: int) -> Optional[User]:
        """Retrieve a user by ID."""
        return self.box.get(id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email."""
        db_query = self.box.query(User.email.equals(email)).build()
        users = db_query.find()
        return users[0] if users else None

    def update_user(self, user: User):
        self.box.put(user)

    def delete_user(self, user_code: str) -> bool:
        """Delete a user."""
        user = self.get_user_by_user_code(user_code)
        if user:
            self.box.remove(user)  # Remove the user entity
            return True
        return False

    def query_in_db(self, field_name: str, field_value: str) -> query:
        return self.box.query(User.user_code.equals(field_value))

    def get_all_users(self) -> List[User]:
        """Fetch all users."""
        return self.box.get_all()
