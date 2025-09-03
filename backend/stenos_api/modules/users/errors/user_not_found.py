class UserNotFound(Exception):
    DETAIL = "User not found"
    ERROR_TYPE = "USER_NOT_FOUND"

    def __init__(self):
        self.message = self.DETAIL
        super().__init__(self.message)