
from stenos_api.modules.auth.schemas.responses.permissions import Permissions

class PermissionsService:

    def __init__(self, permissions_repository):
        self.permissions_repository = permissions_repository


    async def get_user_permissions(self, user_id) -> Permissions:
        return Permissions(
            roles=await self.permissions_repository.get_user_roles(user_id),
            scopes=await self.permissions_repository.get_user_scopes(user_id)
        )