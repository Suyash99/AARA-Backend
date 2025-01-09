from rvc_python.infer import RVCInference
from app.utils.constants import RVC_MODEL_MAP
import os
import requests
import zipfile
import logging

logger = logging.getLogger('main')

def ensure_assets_for_assistant():
    return None

def generate_assistant_response(assistant_name:str):
    if not assistant_name.upper() in RVC_MODEL_MAP:
        logger.error(f"Input assistant - {assistant_name}, in model- {RVC_MODEL_MAP.keys()}")
        raise Exception(f"Assistant for {assistant_name} not found!")

    rvc = RVCInference(device="cuda:0")
    rvc.load_model("path/to/model.pth")
    #convert to edge -> Input.mp3 generate ->
    rvc.infer_file("input.wav", "output.wav")

def download_and_extract(url, folder, model_name):
    if not os.path.exists(f"{folder}/{model_name}"):
        # Download the model
        response = requests.get(url)
        zip_path = f"{folder}/{model_name}.zip"
        with open(zip_path, 'wb') as file:
            file.write(response.content)

        # Extract the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(f"{folder}/{model_name}")

        os.remove(zip_path)  # Remove the zip file after extraction
