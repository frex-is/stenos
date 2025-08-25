from typing import List

from pydantic import BaseModel

from stenos_api.core.schemas.http_methods import HttpMethod
from stenos_api.core.schemas.links import Link
from stenos_api.modules.auth.constants.AuthHateoasDescription import AuthHateoasDescription
from stenos_api.modules.auth.constants.AuthHateoasRelation import AuthHateoasRelation
from stenos_api.modules.auth.routes.routes import AuthRoutes


class RegisterSuccessful(BaseModel):
    user_id: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool

    links: List[Link] = [
        Link(
            href=AuthRoutes.LOGIN,
            relation=AuthHateoasRelation.LOGIN,
            method=HttpMethod.POST,
            description=AuthHateoasDescription.LOGIN
        ),
        Link(
            href=AuthRoutes.VERIFY_EMAIL,
            relation=AuthHateoasRelation.VERIFY_EMAIL,
            method=HttpMethod.POST,
            description=AuthHateoasDescription.VERIFY_EMAIL
        ),
        Link(
            href=AuthRoutes.RESEND_VERIFICATION_EMAIL,
            relation=AuthHateoasRelation.RESEND_VERIFICATION_EMAIL,
            method=HttpMethod.POST,
            description=AuthHateoasDescription.RESEND_VERIFICATION_EMAIL
        ),
    ]
