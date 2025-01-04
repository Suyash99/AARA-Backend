from objectbox import Store
from app.models.user import User
from typing import Generator

def create_box():
    # Instantiate the store first
    store = Store()
    return store.box(User), store  # Return both the box and the store

def get_box() -> Generator:
    box, store = create_box()  # Unpack both box and store
    try:
        yield box
    finally:
        if store:
            store.close()  # Close the store directly