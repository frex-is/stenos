from fastapi import Depends, status, HTTPException, APIRouter

from stenos_api.core.configurations.logging import logger

from stenos_api.modules.auth.errors.invalid_credentials import InvalidCredentials
from stenos_api.modules.auth.schemas.requests.login import LoginRequest
from stenos_api.modules.auth.schemas.responses.login_sucessful import LoginSuccessful
from stenos_api.modules.auth.services.auth_service import AuthService
from stenos_api.modules.users.errors.user_not_found import UserNotFound
from stenos_api.modules.users.services.user_services import UserService
from stenos_api.modules.auth.routes.routes import AuthRoutes

login_router = APIRouter(tags=["auth"])

@login_router.post(
    AuthRoutes.LOGIN,
    response_model=LoginSuccessful,
    status_code=status.HTTP_200_OK,
    responses = {
        status.HTTP_200_OK: {"description": "User logged in successfully"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Input validation failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def login(
    payload: LoginRequest,
    user_service: UserService = Depends(UserService),
    auth_service: AuthService = Depends(AuthService)
):
    """
    Login a user.

    Raises:
        HTTPException 401: If invalid credentials
        HTTPException 500: If unknown error occurs
    """
    logger.debug(
        "🔑 Login attempt",
        email=payload.email
    )

    user = await user_service.get_user_by_email(payload.email)

    if user is None:
        logger.warning(
            "❌ Login failed - user not found",
            email=payload.email,
            error_type=UserNotFound.DETAIL
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=InvalidCredentials.DETAIL
        )

    if not auth_service.verify_password(payload.plain_password, user.hashed_password):
        logger.warning(
            "❌ Login failed - invalid credentials",
            email=payload.email
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=InvalidCredentials.DETAIL
        )

    # access_token=auth_service.create_access_token_for_user(user)

    return LoginSuccessful(
        user_id=user.id
    )