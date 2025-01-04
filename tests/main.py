from objectbox import Entity, Id, Store, String
from pydantic import ConfigDict

from objectbox import Entity
from typing import Optional
from app.models.baseModel import BaseModel

from objectbox import Entity
from typing import Optional


@Entity()
class User:
    username: str = Id()
    user_code: str
    email: str
    password: str
    colour_code: str
    user_photo_bytes: str
    model_config = arbitrary_types_allowed=True


@Entity()
class Person:
    id = Id
    name = String


# The ObjectBox Store represents a database; keep it around...
store = Store()

# Get a box for the "Person" entity; a Box is the main interaction point with objects and the database.
box = store.box(User)
user = User(
    username='Random',
    user_code='Random',
    email='Random',
    password='Random',
    colour_code='Random',
    user_photo_bytes='Random',
)
id = box.put(user)
print(id)
user = box.get(id)
print(user)

# person = Person(name = "Joe Green")
# id = box.put(person)  # Create
# person = box.get(id)  # Read
# person.name = "Joe Black"
# box.put(person)       # Update
# box.remove(person)    # Delete
