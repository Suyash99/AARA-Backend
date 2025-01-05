class ResponseException(Exception):

    def __init__(self, message: str, status_code: int, exception: Exception = None):
        super().__init__(message, exception)
        self.exception = exception
        self.message = message
        self.status_code = status_code

    def __str__(self):
        base_message = f"Status Code: {self.status_code}, Message: {self.message}"
        if self.exception:
            return f"{base_message}, Original Exception: {repr(self.exception)}"
        return base_message