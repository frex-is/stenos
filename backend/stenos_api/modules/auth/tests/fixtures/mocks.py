from pytest import fixture
from unittest.mock import Mock

from stenos_api.modules.auth.services.auth_service import AuthService

@fixture
def mock_auth_service() -> Mock:
    return Mock(spec=AuthService)

@fixture
def mock_crypt_context(monkeypatch) -> Mock:
    mock_crypt_context = Mock()

    monkeypatch.setattr(AuthService, "_password_hashing_context", mock_crypt_context)

    return mock_crypt_context