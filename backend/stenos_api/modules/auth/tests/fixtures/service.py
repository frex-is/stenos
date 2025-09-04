from pytest import fixture

from stenos_api.modules.auth.services.token_service import TokenService


@fixture
def token_service(mock_permissions_service) -> TokenService:
    return TokenService(
        permissions_service=mock_permissions_service,
        secret_key="MySuperSecretKey123!",
        algorithm="HS256",
        access_token_expiration_minutes=60,
        refresh_token_expiration_minutes=60 * 24 * 7
    )