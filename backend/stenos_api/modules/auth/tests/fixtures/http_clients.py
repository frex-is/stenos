from pytest import fixture
from fastapi.testclient import TestClient

from stenos_api.modules.auth.services.auth_service import AuthService
from stenos_api.modules.users.services.user_services import UserService


@fixture
def auth_api_client(mock_user_service, mock_auth_service):
    from fastapi import FastAPI
    from stenos_api.modules.auth.routes.router import auth_router

    application = FastAPI()

    application.include_router(auth_router)
    # TODO refactor this

    async def override_user_service():
        return mock_user_service

    async def override_auth_service():
        return mock_auth_service

    application.dependency_overrides[UserService] = override_user_service
    application.dependency_overrides[AuthService] = override_auth_service

    for route in application.routes:
        print(f"Route: {route.path}, Methods: {route.methods}")

    return TestClient(application)
