# App Info
APP_ID = 'aara'
APP_NAME = 'AARA'

# RVC
RVC_FOLDER = "rvc"
RVCMD_FOLDER = "rvcmd"

RVC_MODEL_MAP = {
    'MIKU': {
        'url': "https://huggingface.co/juuxn/RVCModels/resolve/main/miku222333333.zip",
        'model_name': "miku222333333.pth",
    },
    'HOSHINO': {
        'url': 'https://huggingface.co/juuxn/RVCModels/resolve/main/Ai_Hoshino_(From_Oshi_no_Ko)_(RVC_v2)_300_Epoch.zip',
        'model_name': 'AiHoshino.pth'
    },
    'GLADOS': {
        'url': 'https://huggingface.co/juuxn/RVCModels/resolve/main/glados2333333.zip',
        'model_name': "glados2333333.pth"
    }
}

#Gemini
GEMINI_1_FLASH = 'gemini-1.5-flash'
GEMINI_2_FLASH = 'gemini-2.0-flash-exp'

# Uploads base folder
UPLOAD_DIR = 'uploads'
USER_FOLDER = 'users'
ASSISTANT_FOLDER = 'assistants'

# API Info
API_VERSION = 'v1'

# Server Info
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8000
SERVER_BASE_URL = f'{SERVER_IP}:{SERVER_PORT}/'

# Encryption Keys
AES_ENCRY = {
    'key': b'B9CF1133E770E069695ZX8E6F4F0B9B5'
}
HMAC_ENCRY = {
    'key': 'Some random text goes here!'
}

# User exception message
USER_EXCEPTION_ERRORS = {
    'VALID_USERNAME': "Username must be at least 3 characters long",
    'VALID_UNIQUE_EMAIL': "Email must be unique",
    'VALID_UNIQUE_USER_CODE': "User code must be unique"
}
