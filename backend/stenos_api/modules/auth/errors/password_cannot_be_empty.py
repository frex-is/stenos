class PasswordCannotBeEmpty(Exception):
    DETAIL = "Password cannot be empty"
    ERROR_TYPE = "PASSWORD_CANNOT_BE_EMPTY"

    def __init__(self):
        self.message = self.DETAIL
        super().__init__(self.message)