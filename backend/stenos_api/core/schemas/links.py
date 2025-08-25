from typing import Optional

from pydantic import BaseModel

from stenos_api.core.schemas.http_methods import HttpMethod


class Link(BaseModel):
    href: str
    relation: str
    method: HttpMethod
    description: Optional[str] = None

    class Config:
        use_enum_values = True