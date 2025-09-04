class InvalidTokenError(Exception):
    DETAIL = "Invalid token"
    ERROR_TYPE = "invalid_token_error"

    def __init__(self):
        self.message = self.DETAIL
        super().__init__(self.message)