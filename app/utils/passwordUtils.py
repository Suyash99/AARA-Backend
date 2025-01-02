from app.mapper.userResponse import UserResponse
from app.exceptions.tokenException import TokenException
from typing import Optional
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
    def generate_hashed_token(user_response: UserResponse) -> str:
        try:
            # Convert UserResponse object to a JSON string
            user_data = user_response.model_dump_json()

            token_payload = user_data

            token_payload.expiry_time = (time.time() * 1000) + (1 * 7 * 24 * 60 * 60 * 1000)  # Expire in 1 week

            # Create a SHA256 hash of the serialized data
            hash_object = hashlib.sha256(token_payload.encode('utf-8'))

            # Encode the hash in Base64 for a URL-safe token
            token = base64.urlsafe_b64encode(hash_object.digest()).decode('utf-8')

            return token
        except Exception as e:
            logger.error(f"error while generating hash:: {e}")
            raise TokenException('Error while generating hash- ' + e)


    @staticmethod
    def verify_hashed_token(token: str) -> Optional[dict]:
        """
        Verify the hashed token.
        :param token: The token to verify.
        :return: Decoded payload if valid, None otherwise.
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
                logger.error("Token has expired.")
                raise TokenException("Token has expired!", 403)

            # Recompute the hash from the payload and verify
            original_payload = json.dumps(
                {k: v for k, v in token_payload.items() if k != "expiry_time"}
            )
            hash_object = hashlib.sha256(original_payload.encode('utf-8')).digest()
            recomputed_hash = base64.urlsafe_b64encode(hash_object).decode('utf-8')

            if recomputed_hash != token:
                logger.error("Token hash verification failed.")
                raise TokenException("Token hash verification failed", 401)

            return token_payload

        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return TokenException(f"Error verifying token: {e}")