from pathlib import Path

UPLOAD_DIR = Path("../uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_image(filename:str, filebytes: bytes) -> bytes:
    file_path = UPLOAD_DIR / filename
    with file_path.open("wb") as buffer:
        buffer.write(filebytes)

    return file_path.read_bytes()