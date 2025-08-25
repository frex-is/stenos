from passlib.context import CryptContext

from stenos_api.modules.auth.errors.password_cannot_be_empty import PasswordCannotBeEmpty
from stenos_api.modules.auth.errors.password_too_long import PasswordTooLong

class AuthService:
    BCRYPT_MAX_PASSWORD_LENGTH = 72

    _password_hashing_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
        bcrypt__default_rounds=12
    )


    @staticmethod
    def hash_password(plain_password: str) -> str:
        """
        Hash a password using BCrypt

        Args:
            plain_password (str): The password to hash (72 characters max, due to BCrypt limitation. Longer passwords raise PasswordTooLong)
        
        Security Note:
            BCrypt silently truncates at 72 bytes (ASCII chars). We explicitly
            validate to prevent partial password attacks.
        """
        if not plain_password:
            raise PasswordCannotBeEmpty()
        
        if len(plain_password) > AuthService.BCRYPT_MAX_PASSWORD_LENGTH:
            raise PasswordTooLong()
        
        return AuthService._password_hashing_context.hash(plain_password)


    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return AuthService._password_hashing_context.verify(plain_password, hashed_password)


    @staticmethod
    def is_hashed_password(hashed_password: str) -> bool:
        if not hashed_password:
            return False
        
        return AuthService._password_hashing_context.identify(hashed_password) == "bcrypt"