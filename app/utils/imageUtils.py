from pathlib import Path
import os
import logging

logger = logging.getLogger('main')

UPLOAD_DIR = Path("../uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_image(filename: str, filebytes: bytes) -> bytes:
    file_path = UPLOAD_DIR / filename
    with file_path.open("wb") as buffer:
        buffer.write(filebytes)

    return file_path.read_bytes()


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
