from pydantic import BaseModel, Field
from typing import List

class Permissions:
    roles: List[str] = Field(
        default_factory=list,
        description="List of user's global roles",
        example=["user", "premium"],
    )

    scopes: List[str] = Field(
        default_factory=list,
        description="List of granular permissions (OAuth2 scopes)",
        example=["users:read", "posts:write", "billing:manage"],
    )
