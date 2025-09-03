import datetime

from jwt import encode
from datetime import datetime
from uuid import uuid4

from stenos_api.modules.users.schemas.responses.user_response import UserResponse

from stenos_api.modules.auth.services.permissions_service import PermissionsService

class TokenService:

    def __init__(
            self,
            permissions_service: PermissionsService,
            secret_key: str,
            algorithm: str = "HS256",
            token_expiration_minutes: int = 60
    ):
        self.permissions_service = permissions_service
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiration_minutes = token_expiration_minutes

    def create_access_token(self, user: UserResponse) -> str:
        permissions = self.permissions_service.get_user_permissions(user.id)

        payload = {
            "sub": user.id,
            "exp": self._get_expiration_time(),
            "iat": self._get_current_time(),
            "jti": str(uuid4),

            "roles": permissions.roles,
            "scopes": permissions.scopes,
            "full_name": f"{user.first_name} {user.last_name}",
            "email": user.email,

            "token_type": "access",
            "iss": "stenos-api",
            "aud": "stenos-client"
        }

        return encode(payload, self.secret_key, algorithm=self.algorithm)

    @staticmethod
    def _get_current_time():
        return datetime.now(datetime.UTC)

    def _get_expiration_time(self):
        return datetime.now(datetime.UTC) + datetime.timedelta(minutes=self.token_expiration_minutes)