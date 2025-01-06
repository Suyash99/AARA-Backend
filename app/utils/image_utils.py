import logging
import os

logger = logging.getLogger('main')

def save_image(file_bytes: bytes, file_name: str, directory: str) -> str | None:
    if file_bytes is None:
        return None
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f"{file_name}.jpg")
    with open(file_path, "wb") as file:
        file.write(file_bytes)
        return file_path


def delete_image(image_path: str):
    try:
        print(f"path- {UPLOAD_DIR / image_path}")
        if os.path.exists(UPLOAD_DIR / image_path):
            os.remove(image_path)  # Delete the file
            logger.info(f"Image {image_path} deleted successfully.")
        else:
            logger.info(f"The file {image_path} does not exist.")
    except Exception as e:
        logger.error(f"Error occurred while deleting the image: {str(e)}")
        raise Exception(f"Error occured while deleting the image: {str(e)}")
