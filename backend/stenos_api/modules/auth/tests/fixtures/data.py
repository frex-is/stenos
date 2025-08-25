from pytest import fixture
from typing import Any

from stenos_api.modules.auth.schemas.requests.register import RegisterRequest

@fixture
def valid_register_request() -> dict[str, Any]:
    return RegisterRequest(
        first_name="John",
        last_name="Smith",
        email="john.smith@example.com",
        plain_password="MySuperSecurePassword123!"
    ).model_dump()
