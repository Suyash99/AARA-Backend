import random
import string

class GenerateCodeForId:
    @staticmethod
    def generate_random_code(length: int) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
