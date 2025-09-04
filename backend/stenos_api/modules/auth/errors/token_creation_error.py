class TokenCreationError(Exception):
    DETAIL = "Failed to create token"
    ERROR_TYPE = "token_creation_error"

    def __init__(self, exception: Exception):
        self.message = f"{self.DETAIL}: {exception}"
        super().__init__(self.message)