from pytest import mark, raises
from unittest.mock import Mock

from stenos_api.modules.auth.errors.password_cannot_be_empty import PasswordCannotBeEmpty
from stenos_api.modules.auth.errors.password_too_long import PasswordTooLong
from stenos_api.modules.auth.services.auth_service import AuthService
from stenos_api.modules.auth.tests.fixtures.mocks import mock_crypt_context # noqa: F401  # Required for pytest fixture (indirect usage) 

class TestAuthService:

    @mark.security
    def test_hash_valid_password(self, mock_crypt_context: Mock):
        password_to_hash = "SecurePassword123!"
        mock_crypt_context.hash.return_value = "hashed_password"

        hashed_password = AuthService.hash_password(password_to_hash)

        mock_crypt_context.hash.assert_called_once_with(password_to_hash)
        assert hashed_password == "hashed_password"
    
    @mark.security
    def test_hash_password_invalid_cause_empty_password(self, mock_crypt_context: Mock):
        empty_password_to_hash = ""

        with raises(PasswordCannotBeEmpty) as execution_info:
            AuthService.hash_password(empty_password_to_hash)

        mock_crypt_context.hash.assert_not_called()
        assert execution_info.value.message == PasswordCannotBeEmpty().message


    @mark.security
    def test_hash_password_invalid_cause_to_long(self, mock_crypt_context: Mock):
        """
        Verify BCrypt's 72 character limit enforcement

        BCrypt truncates before 72 characters without warning
        This test ensure we fail explicitly rather than silently
        """
        long_password_to_hash = "a" * 73

        with raises(PasswordTooLong) as execution_info:
            AuthService.hash_password(long_password_to_hash)

        mock_crypt_context.hash.assert_not_called()
        assert execution_info.value.message == PasswordTooLong().message
