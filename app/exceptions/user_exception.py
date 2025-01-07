class UserExceptionError(Exception):
    """
    Custom exception for validation errors.
    """

    def __init__(self, message: str, field: str = None):
        """
        Initialize the exception with an error message and optional field name.

        Args:
            message (str): The error message.
            field (str, optional): The name of the field causing the error. Defaults to None.
        """
        super().__init__(message)
        self.field = field

    def __str__(self):
        if self.field:
            return f"Validation Error on '{self.field}': {self.args[0]}"
        return f"Validation Error: {self.args[0]}"
