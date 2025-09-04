from pytest import mark

from stenos_api.modules.auth.tests.fixtures.data import valid_permissions # noqa: F401  # Required for pytest fixture (indirect usage)
from stenos_api.modules.auth.tests.fixtures.service import token_service # noqa: F401  # Required for pytest fixture (indirect usage)
from stenos_api.modules.auth.tests.fixtures.mocks import mock_permissions_service # noqa: F401  # Required for pytest fixture (indirect usage)
from stenos_api.modules.users.tests.fixtures.data import valid_user_response # noqa: F401  # Required for pytest fixture (indirect usage)


class TestTokenServiceIntegration:

    @mark.integration
    @mark.security
    @mark.asyncio
    async def test_create_access_token_successful(
        self,
        token_service,
        mock_permissions_service,
        valid_user_response,
        valid_permissions
    ):
        mock_permissions_service.get_user_permissions.return_value = valid_permissions

        token = await token_service.create_access_token(valid_user_response)

        decoded_payload = token_service.decode_and_validate_token(token)

        # assert decoded_payload["sub"] == valid_user_response["user_id"]

    @mark.integration
    @mark.security
    @mark.asyncio
    async def test_create_refresh_token_successful(
        self,
        token_service,
        mock_permissions_service,
        valid_user_response,
        valid_permissions
    ):
        mock_permissions_service.get_user_permissions.return_value = valid_permissions

        token = await token_service.create_refresh_token(valid_user_response)

        # TODO wait for decode token implementation


    @mark.integration
    @mark.security
    @mark.asyncio
    async def test_refresh_token_has_longer_expiration_than_access_token(
        self,
        token_service,
        mock_permissions_service,
        valid_user_response,
        valid_permissions
    ):
        mock_permissions_service.get_user_permissions.return_value = valid_permissions

        access_token = await token_service.create_access_token(valid_user_response)
        refresh_token = await token_service.create_refresh_token(valid_user_response)

        # TODO wait for decode token implementation