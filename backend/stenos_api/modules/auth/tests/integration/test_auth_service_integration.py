from bcrypt import hashpw, gensalt, checkpw
from time import time
from pytest import mark, raises

from stenos_api.modules.auth.errors.password_cannot_be_empty import PasswordCannotBeEmpty
from stenos_api.modules.auth.errors.password_too_long import PasswordTooLong
from stenos_api.modules.auth.services.auth_service import AuthService

class TestAuthServiceIntegration:

    @mark.security
    @mark.integration
    def test_hash_and_verify_password(self):
        valid_password = "SecurePassword123!"

        hashed_password = AuthService.hash_password(valid_password)

        assert AuthService.verify_password(valid_password, hashed_password)
        assert not AuthService.verify_password("InvalidPassword", hashed_password)

      
    @mark.security
    @mark.integration
    def test_verify_with_existing_bcrypt_hashed_password(self):
        valid_password = "MySecureP@ssw0rd"
        bcrypt_hash = hashpw(valid_password.encode(), gensalt()).decode()

        assert AuthService.verify_password(valid_password, bcrypt_hash)
        assert not AuthService.verify_password("InvalidPassword", bcrypt_hash)


    @mark.security
    @mark.integration
    def test_hash_salt_should_be_unique(self):
        valid_password = "SecurePassword123!"

        hashed_password_1 = AuthService.hash_password(valid_password)
        hashed_password_2 = AuthService.hash_password(valid_password)

        assert hashed_password_1 != hashed_password_2


    @mark.security
    @mark.integration
    def test_hashing_vulnerability_on_time_attack(self):
        valid_password = "SecurePassword123!"

        start_time = time()

        AuthService.hash_password(valid_password)

        end_time = time()

        # Ensure hashing takes at least 0.1 seconds to prevent timing attacks
        assert end_time - start_time >= 0.1


    @mark.security
    @mark.integration
    def test_is_hashed_password(self):
        valid_password = "SecurePassword123!"

        hashed_password = AuthService.hash_password(valid_password)

        assert AuthService.is_hashed_password(hashed_password)
        assert not AuthService.is_hashed_password(valid_password)


    @mark.security
    @mark.integration
    def test_should_throw_password_cannot_be_empty_exception(self):
        empty_password = ""

        with raises(PasswordCannotBeEmpty) as execution_info:
            AuthService.hash_password(empty_password)

        assert execution_info.value.message == PasswordCannotBeEmpty().message

    
    @mark.security
    @mark.integration
    def test_should_throw_password_too_long_exception(self):
        long_password = "a" * 73

        with raises(PasswordTooLong) as execution_info:
            AuthService.hash_password(long_password)

        assert execution_info.value.message == PasswordTooLong().message
