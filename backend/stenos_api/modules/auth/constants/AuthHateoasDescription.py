from enum import Enum


class AuthHateoasDescription(str, Enum):
    LOGIN = "Login to your account"
    VERIFY_EMAIL = "Verify your email"
    RESEND_VERIFICATION_EMAIL = "Resend verification email"
    REFRESH_TOKEN = "Get new access token"