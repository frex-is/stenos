from fastapi import Depends, status, HTTPException

from stenos_api.core.configurations.logging import logger

from . import auth_router
from stenos_api.modules.auth.schemas.requests.register import RegisterRequest
from stenos_api.modules.auth.services.auth_service import AuthService
from stenos_api.modules.auth.schemas.responses.register_successful import RegisterSuccessful
from stenos_api.modules.auth.routes.routes import AuthRoutes

from stenos_api.modules.users.services.user_services import UserService
from stenos_api.modules.users.errors.user_already_exists import UserAlreadyExists
from stenos_api.modules.users.schemas.requests.user_create import UserCreate


@auth_router.post(
    AuthRoutes.REGISTER,
    response_model=RegisterSuccessful, 
    status_code=status.HTTP_201_CREATED,
    responses = {
        status.HTTP_201_CREATED: {"description": "User registered successfully"},
        status.HTTP_409_CONFLICT: {"description": "User already exists"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Input validation failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def register(
    payload: RegisterRequest,
    user_service: UserService = Depends(UserService),
    auth_service: AuthService = Depends(AuthService)
) -> RegisterSuccessful:
    """
    Register a new user.

    Raises:
        HTTPException 400: If input validation fails
        HTTPException 409: If email already registered
        HTTPException 500: If unknown error occurs
    """
    logger.debug(
        "🔑 Register attempt", 
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email
    )

    if await user_service.get_user_by_email(payload.email) is not None:
        logger.warning(
            "🚨 Duplicate registration",
            email=payload.email,
            error_type=UserAlreadyExists.ERROR_TYPE
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=UserAlreadyExists.DETAIL
        )

    try:
        user_create = UserCreate(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            hashed_password=auth_service.hash_password(payload.plain_password)
        )

        user = await user_service.create_user(user_create)

    except UserAlreadyExists:
        logger.warning(
            "🚨 Duplicate registration",
            email=payload.email,
            error_type=UserAlreadyExists.ERROR_TYPE
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=UserAlreadyExists.DETAIL
        )
    
    except Exception as exception:
        logger.critical(
            "💥 Unknown internal server error",
            error=str(exception),
            exception_type=type(exception).__name__,
            stack_info=True
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exception)
        )

    return RegisterSuccessful(
        user_id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_verified=user.is_verified,
    )
