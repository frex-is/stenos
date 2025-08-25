from stenos_api.modules.users.schemas.requests.user_create import UserCreate
from stenos_api.modules.users.schemas.responses.user_response import UserResponse

class UserService:

    def __init__(self):
        pass

    async def create_user(self, user: UserCreate) -> UserResponse:
        # TODO
        return UserResponse(
            id="1",
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_verified=False
        )

    async def get_user_by_email(self, email: str) -> UserResponse:
        # TODO
        return None