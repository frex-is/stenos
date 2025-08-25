from http import HTTPStatus

from pytest import mark

from stenos_api.modules.auth.constants.AuthHateoasDescription import AuthHateoasDescription
from stenos_api.modules.auth.constants.AuthHateoasRelation import AuthHateoasRelation
from stenos_api.modules.auth.routes.routes import AuthRoutes
from stenos_api.modules.auth.tests.fixtures.http_clients import auth_api_client # noqa: F401  # Required for pytest fixture (indirect usage)
from stenos_api.modules.auth.tests.fixtures.data import valid_register_request # noqa: F401  # Required for pytest fixture (indirect usage)
from stenos_api.modules.users.errors.user_already_exists import UserAlreadyExists
from stenos_api.modules.users.tests.fixtures.mocks import mock_user_service # noqa: F401  # Required for pytest fixture (indirect usage)
from stenos_api.modules.users.tests.fixtures.data import valid_user_response # noqa: F401  # Required for pytest fixture (indirect usage)
from stenos_api.modules.auth.tests.fixtures.mocks import mock_auth_service # noqa: F401  # Required for pytest fixture (indirect usage)

class TestRegisterEndpoint:
    
    @mark.integration
    def test_register_successful_with_correct_data(
        self, 
        auth_api_client, 
        mock_auth_service, 
        mock_user_service, 
        valid_user_response, 
        valid_register_request
    ):
        mock_user_service.get_user_by_email.return_value = None
        mock_user_service.create_user.return_value = valid_user_response
        mock_auth_service.hash_password.return_value = "hashed_password"

        response = auth_api_client.post(AuthRoutes.REGISTER, json=valid_register_request)

        assert response.status_code == HTTPStatus.CREATED

        response_payload = response.json()

        assert "user_id" in response_payload
        assert response_payload["first_name"] == valid_register_request["first_name"]
        assert response_payload["last_name"] == valid_register_request["last_name"]
        assert response_payload["email"] == valid_register_request["email"]
        assert response_payload["is_verified"] is False


    @mark.integration
    def test_register_hateoas_links_present(
        self,
        auth_api_client,
        mock_auth_service,
        mock_user_service,
        valid_user_response,
        valid_register_request
    ):
        mock_user_service.get_user_by_email.return_value = None
        mock_user_service.create_user.return_value = valid_user_response
        mock_auth_service.hash_password.return_value = "hashed_password"

        response = auth_api_client.post(AuthRoutes.REGISTER, json=valid_register_request)

        response_payload = response.json()

        assert "links" in response_payload

        link_by_relation = { link["relation"]: link for link in response_payload["links"] }

        assert AuthHateoasRelation.LOGIN in link_by_relation
        assert link_by_relation[AuthHateoasRelation.LOGIN]["href"] == AuthRoutes.LOGIN
        assert link_by_relation[AuthHateoasRelation.LOGIN]["method"] == "POST"
        assert link_by_relation[AuthHateoasRelation.LOGIN]["description"] == AuthHateoasDescription.LOGIN

        assert AuthHateoasRelation.VERIFY_EMAIL in link_by_relation
        assert link_by_relation[AuthHateoasRelation.VERIFY_EMAIL]["href"] == AuthRoutes.VERIFY_EMAIL
        assert link_by_relation[AuthHateoasRelation.VERIFY_EMAIL]["method"] == "POST"
        assert link_by_relation[AuthHateoasRelation.VERIFY_EMAIL]["description"] == AuthHateoasDescription.VERIFY_EMAIL

        assert AuthHateoasRelation.RESEND_VERIFICATION_EMAIL in link_by_relation
        assert link_by_relation[AuthHateoasRelation.RESEND_VERIFICATION_EMAIL]["href"] == AuthRoutes.RESEND_VERIFICATION_EMAIL
        assert link_by_relation[AuthHateoasRelation.RESEND_VERIFICATION_EMAIL]["method"] == "POST"
        assert link_by_relation[AuthHateoasRelation.RESEND_VERIFICATION_EMAIL]["description"] == AuthHateoasDescription.RESEND_VERIFICATION_EMAIL


    @mark.integration
    @mark.asyncio
    async def test_register_user_already_exists(
            self,
            auth_api_client,
            mock_auth_service,
            mock_user_service,
            valid_user_response,
            valid_register_request
    ):
        mock_user_service.get_user_by_email.return_value = valid_user_response

        response = auth_api_client.post(AuthRoutes.REGISTER, json=valid_register_request)

        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json() == { "detail": UserAlreadyExists.DETAIL }


    @mark.parametrize("invalid_request_fields, expected_error", [
        ({"email": "invalid-email"}, "email")
    ])
    @mark.integration
    @mark.asyncio
    async def test_register_request_validation_fails(
        self,
        auth_api_client,
        valid_register_request,
        invalid_request_fields,
        expected_error
    ):
        invalid_request = {**valid_register_request, **invalid_request_fields}

        response = auth_api_client.post(AuthRoutes.REGISTER, json=invalid_request)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
