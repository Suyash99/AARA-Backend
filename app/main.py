import objectbox.model
from objectbox import Model, Entity


# Define a simple model
@Entity
class User:
    username: str
    email: str
    password: str
    user_code: str
    colour_code: str

# Create a model instance
model = Model()
print("ObjectBox model created successfully!")
