from pytest import fixture
from typing import Any

from stenos_api.modules.users.schemas.responses.user_response import UserResponse

@fixture
def valid_user_response() -> UserResponse:
    return UserResponse(
        id="1",
        email="john.smith@example.com",
        first_name="John",
        last_name="Smith",
        is_verified=False,
        hashed_password="hashed_password"
    )
