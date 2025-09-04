from pytest import fixture
from unittest.mock import Mock

from stenos_api.modules.auth.services.auth_service import AuthService
from stenos_api.modules.auth.services.permissions_service import PermissionsService
from stenos_api.modules.auth.services.token_service import TokenService


@fixture
def mock_auth_service() -> Mock:
    return Mock(spec=AuthService)

@fixture
def mock_crypt_context(monkeypatch) -> Mock:
    mock_crypt_context = Mock()

    monkeypatch.setattr(AuthService, "_password_hashing_context", mock_crypt_context)

    return mock_crypt_context

@fixture
def mock_token_service() -> Mock:
    return Mock(spec=TokenService)

@fixture
def mock_permissions_service() -> Mock:
    return Mock(spec=PermissionsService)
