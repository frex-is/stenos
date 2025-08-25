class PasswordTooLong(Exception):
    DETAIL = "Password cannot be longer than 72 characters"
    ERROR_TYPE = "PASSWORD_TOO_LONG"

    def __init__(self):
        self.message = self.DETAIL
        super().__init__(self.message)