from app.mapper.user_response import UserResponse
from app.exceptions.tokenException import TokenException
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from app.utils.constants import AES_ENCRY
import bcrypt
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
    def decrypt_aes_encoded_text(encrypted_text: str) -> str:
        try:
            # Decode the Base64 encoded ciphertext
            ciphertext = base64.b64decode(encrypted_text)

            # Create AES cipher in ECB mode
            cipher = Cipher(algorithms.AES(AES_ENCRY['key']), modes.ECB(), backend=default_backend())
            decryptor = cipher.decryptor()

            # Decrypt the ciphertext
            decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

            # Remove padding
            unpadder = padding.PKCS7(128).unpadder()
            decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

            # Return the decrypted (unpadded) data as a string
            return decrypted_data.decode('utf-8')

        except Exception as e:
            raise TokenException(f"Error decrypting data: {e}", 400)

    @staticmethod
    def generate_hashed_token(user_response: UserResponse) -> str:
        try:
            # Convert UserResponse object to a JSON string
            user_data = json.loads(user_response.model_dump_json())
            token_payload = {key: value for key, value in user_data.items() if key != 'user_photo_bytes'} #Exclude from token

            token_payload['expiry_time'] = (time.time() * 1000) + (1 * 7 * 24 * 60 * 60 * 1000)   # Expire in 1 week

            plaintext = json.dumps(token_payload).encode("utf-8")

            # Add padding
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plaintext) + padder.finalize()

            # Encrypt
            cipher = Cipher(algorithms.AES(AES_ENCRY['key']), modes.ECB(), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            # Base64 encode the ciphertext
            return base64.urlsafe_b64encode(ciphertext).decode("utf-8")
        except Exception as e:
            logger.error(f"error while generating hash:: {e}")
            raise TokenException(f"Error while generating hash- {e}", 400)

    @staticmethod
    def verify_hashed_token(token: str) -> None:
        """
        Verify the hashed token.
        :param token: The token to verify.
        """
        try:
            ciphertext = base64.urlsafe_b64decode(token)

            # Decrypt
            cipher = Cipher(algorithms.AES(AES_ENCRY['key']), modes.ECB(), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

            # Remove padding
            unpadder = padding.PKCS7(128).unpadder()
            decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

            # Convert JSON string back to dict
            token_payload = json.loads(decrypted_data.decode("utf-8"))

            # Extract expiry time
            expiry_time = token_payload.get("expiry_time")
            if not expiry_time:
                logger.error("Invalid token: Missing expiry time.")
                raise TokenException("Invalid token: Missing expiry time.", 401)

            # Check if the token is expired
            current_time_ms = time.time() * 1000
            if current_time_ms > expiry_time:
                readable_date = datetime.fromtimestamp(expiry_time / 1000).isoformat(sep=" ", timespec="seconds")
                logger.error(f"Token expired at {readable_date}, will return error")
                raise TokenException("Token has expired!", 410)
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            raise TokenException(f"Error verifying token: {e}", 400)