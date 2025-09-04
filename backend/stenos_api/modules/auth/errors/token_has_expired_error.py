class TokenHasExpiredError(Exception):
    DETAIL = "Token has expired"
    ERROR_TYPE = "token_has_expired_error"

    def __init__(self):
        self.message = self.DETAIL
        super().__init__(self.message)