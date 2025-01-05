from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
from app.utils.constants import AES_ENCRY


def encrypt_aes_ecb(plain_text: str, key: bytes) -> str:
    """
    Encrypts the given plaintext using AES in ECB mode.
    :param plain_text: Plain text to encrypt.
    :param key: Encryption key (must be 16, 24, or 32 bytes for AES).
    :return: Encrypted text (Base64 encoded).
    """
    try:
        # Create AES cipher in ECB mode
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad plaintext to be a multiple of 16 bytes (AES block size)
        padder = padding.PKCS7(128).padder()  # 128-bit block size for AES
        padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()

        # Encrypt the padded data
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Return the encrypted ciphertext as base64 encoded string
        return base64.b64encode(ciphertext).decode('utf-8')

    except Exception as e:
        raise Exception(f"Error encrypting data: {e}")


print(encrypt_aes_ecb('letTheGameBegin@009',AES_ENCRY['key']))
