class UserAlreadyExists(Exception):
    DETAIL = "User already exists"
    ERROR_TYPE = "USER_ALREADY_EXISTS"

    def __init__(self):
        self.message = self.DETAIL
        super().__init__(self.message)