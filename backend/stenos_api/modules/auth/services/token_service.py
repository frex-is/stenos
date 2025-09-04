import datetime

from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from uuid import uuid4
from enum import Enum

from stenos_api.modules.users.schemas.responses.user_response import UserResponse
from stenos_api.modules.auth.errors.token_creation_error import TokenCreationError
from stenos_api.modules.auth.services.permissions_service import PermissionsService
from stenos_api.modules.auth.errors.token_has_expired_error import TokenHasExpiredError
from stenos_api.modules.auth.errors.invalid_token_error import InvalidTokenError as TokenServiceInvalidTokenError


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenService:

    def __init__(
        self,
        permissions_service: PermissionsService,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expiration_minutes: int = 60,
        refresh_token_expiration_minutes: int = 60 * 24 * 7
    ):
        self.permissions_service = permissions_service
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiration_minutes = access_token_expiration_minutes
        self.refresh_token_expiration_minutes = refresh_token_expiration_minutes
        self.issuer = "stenos_api"
        self.audience = "stenos_client"


    def decode_and_validate_token(self, token: str) -> dict:
        try:
            return decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer
            )
        except ExpiredSignatureError:
            raise TokenHasExpiredError()
        except InvalidTokenError:
            raise TokenServiceInvalidTokenError()


    async def _create_token(self, user: UserResponse, token_type: TokenType) -> str:
        payload = await self._get_token_payload(user, token_type)

        try:
            return encode(payload, self.secret_key, algorithm=self.algorithm)
        except Exception as exception:
            raise TokenCreationError(exception)


    async def create_refresh_tokens(self, user: UserResponse) -> str:
        return await self._create_token(user, token_type=TokenType.REFRESH)


    async def create_access_token(self, user: UserResponse) -> str:
        return await self._create_token(user, token_type=TokenType.ACCESS)


    async def _get_token_payload(self, user: UserResponse, token_type: TokenType) -> dict[str, str]:
        permissions = await self.permissions_service.get_user_permissions(user.id)

        return {
            "sub": user.id,
            "exp": self._get_expiration_time(token_type),
            "iat": self._get_current_time(),
            "jti": str(uuid4),

            "roles": permissions.roles,
            "scopes": permissions.scopes,
            "full_name": f"{user.first_name} {user.last_name}",
            "email": user.email,

            "token_type": token_type.value,
            "iss": self.issuer,
            "aud": self.audience
        }


    @staticmethod
    def _get_current_time():
        return datetime.now()


    def _get_expiration_time(self, token_type: TokenType):
        token_expiration = (
            self.token_expiration_minutes
            if token_type == TokenType.ACCESS
            else self.refresh_token_expiration_minutes
        )

        return datetime.now() + timedelta(minutes=token_expiration)
