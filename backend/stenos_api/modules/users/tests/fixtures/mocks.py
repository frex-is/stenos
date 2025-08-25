from pytest import fixture
from unittest.mock import AsyncMock

from stenos_api.modules.users.services.user_services import UserService

@fixture
def mock_user_service() -> AsyncMock:
    return AsyncMock(spec=UserService)