class InvalidCredentials(Exception):
    DETAIL = "Email or password is invalid"
    ERROR_TYPE = "invalid_credentials"

    def __init__(self):
        self.message = self.DETAIL
        super().__init__(self.message)