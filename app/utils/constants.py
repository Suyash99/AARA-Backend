# App Info
APP_ID = 'aara'
APP_NAME = 'AARA'

# API Info
API_VERSION = 'v1'

# Server Info
SERVER_IP = '127.0.0.1'
SERVER_PORT =  8000
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
    'VALID_USERNAME':"Username must be at least 3 characters long",
    'VALID_UNIQUE_EMAIL':"Email must be unique",
    'VALID_UNIQUE_USER_CODE':"User code must be unique"
}