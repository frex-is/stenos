from enum import Enum

class AuthHateoasRelation(str, Enum):
    LOGIN = "login"
    VERIFY_EMAIL = "verify-email"
    RESEND_VERIFICATION_EMAIL = "resend-verification-email"
    REFRESH_TOKEN = "refresh-token"