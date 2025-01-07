class AuthException(Exception):
    """
    Custom exception class for token-related errors.
    """

    def __init__(self, message: str, code: int = 400):
        """
        Initialize the TokenException with a message and an optional code.

        :param message: Error message describing the issue.
        :param code: HTTP status code or custom error code. Defaults to 400.
        """
        self.message = message
        self.status_code = code
        super().__init__(f"TokenException {code}: {message}")

    def __str__(self):
        """
        String representation of the exception.
        :return: The error message.
        """
        return f"{self.message}, code-  {self.status_code}"
