from app.mapper.userResponse import UserResponse
from app.exceptions.tokenException import TokenException
from typing import Optional
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from app.appConstants import AES_ENCRY
import bcrypt
import hashlib
import base64
import time
import json
import logging
logger = logging.getLogger("main")

class PasswordUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes the given password using bcrypt.
        :param password: Plain text password.
        :return: Hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verifies if the given password matches the hashed password.
        :param password: Plain text password.
        :param hashed_password: Hashed password to compare.
        :return: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def decrypt_aes_encoded_text(ecryp_user_detail:str) -> str:
        try:
            decryptor = Cipher(algorithms.AES(AES_ENCRY['key']), modes.ECB(), backend=default_backend()).decryptor()
            decrypted_data = decryptor.update(ecryp_user_detail) + decryptor.finalize()

            unpadder = padding.PKCS7(128).unpadder()
            unpadded_data = unpadder.update(decrypted_data)
            unpadded_data += unpadder.finalize()
            return unpadded_data.decode('utf-8')
        except Exception as e:
            raise TokenException(f'Error refreshing token', 400)

    @staticmethod
    def generate_hashed_token(user_response: UserResponse) -> str:
        try:
            # Convert UserResponse object to a JSON string
            user_data = json.loads(user_response.model_dump_json())
            user_data['expiry_time'] = (time.time() * 1000) + (1 * 7 * 24 * 60 * 60 * 1000)  # Expire in 1 week
            token_payload = json.dumps(user_data)

            # Create a SHA256 hash of the serialized data
            hash_object = hashlib.sha256(token_payload.encode('utf-8'))

            # Encode the hash in Base64 for a URL-safe token
            token = base64.urlsafe_b64encode(hash_object.digest()).decode('utf-8')

            return token
        except Exception as e:
            logger.error(f"error while generating hash:: {e}")
            raise TokenException(f'Error while generating hash- {e}', 400)

    @staticmethod
    def verify_hashed_token(token: str) -> None:
        """
        Verify the hashed token.
        :param token: The token to verify.
        """
        try:
            # Decode the Base64 token
            decoded_hash = base64.urlsafe_b64decode(token.encode('utf-8'))
            token_payload = json.loads(decoded_hash.decode("utf-8"))

            # Extract expiry time
            expiry_time = token_payload.get("expiry_time")
            if not expiry_time:
                logger.error("Invalid token: Missing expiry time.")
                raise TokenException("Invalid token: Missing expiry time.", 401)

            # Check if the token is expired
            current_time_ms = time.time() * 1000
            if current_time_ms > expiry_time:
                readable_date = datetime.fromtimestamp(expiry_time/1000).isoformat(sep=' ', timespec='seconds')
                logger.error(f"Token expired at {readable_date}, will return error")
                raise TokenException("Token has expired!", 410)
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            raise TokenException(f"Error verifying token: {e}", 400)