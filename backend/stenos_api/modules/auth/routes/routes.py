from enum import Enum

class AuthRoutes(str, Enum):
    LOGIN = "/auth/login"
    REGISTER = "/auth/register"
    VERIFY_EMAIL = "/auth/verify-email"
    RESEND_VERIFICATION_EMAIL = "/auth/resend-verification-email"