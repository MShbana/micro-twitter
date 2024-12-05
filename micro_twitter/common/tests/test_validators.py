from django.core.exceptions import ValidationError
from django.test import TestCase

from micro_twitter.common.validators import (
    LowerCasePasswordValidator,
    NumberPasswordValidator,
    SymbolPasswordValidator,
    UpperCasePasswordValidator,
)


class PasswordValidatorTests(TestCase):

    def setUp(self):
        self.number_validator = NumberPasswordValidator()
        self.uppercase_validator = UpperCasePasswordValidator()
        self.lowercase_validator = LowerCasePasswordValidator()
        self.symbol_validator = SymbolPasswordValidator()

    def test_number_password_validator_valid(self):
        """Test that the password with a digit passes the validator."""
        valid_password = "Password123"
        # Validate the valid password (should not raise an exception).
        self.number_validator.validate(valid_password)

    def test_number_password_validator_invalid(self):
        """Test that the password without a digit fails the validator."""
        invalid_password = "Password"
        # Assert that a ValidationError is raised.
        with self.assertRaises(ValidationError):
            self.number_validator.validate(invalid_password)

    def test_uppercase_password_validator_valid(self):
        """Test that the password with an uppercase letter passes the validator."""
        valid_password = "Password123"
        # Validate the valid password (should not raise an exception).
        self.uppercase_validator.validate(valid_password)

    def test_uppercase_password_validator_invalid(self):
        """Test that the password without an uppercase letter fails the validator."""
        invalid_password = "password123"
        # Assert that a ValidationError is raised.
        with self.assertRaises(ValidationError):
            self.uppercase_validator.validate(invalid_password)

    def test_lowercase_password_validator_valid(self):
        """Test that the password with a lowercase letter passes the validator."""
        valid_password = "Password123"
        # Validate the valid password (should not raise an exception).
        self.lowercase_validator.validate(valid_password)

    def test_lowercase_password_validator_invalid(self):
        """Test that the password without a lowercase letter fails the validator."""
        invalid_password = "PASSWORD123"
        # Assert that a ValidationError is raised.
        with self.assertRaises(ValidationError):
            self.lowercase_validator.validate(invalid_password)

    def test_symbol_password_validator_valid(self):
        """Test that the password with a symbol passes the validator."""
        valid_password = "Password@123"
        # Validate the valid password (should not raise an exception).
        self.symbol_validator.validate(valid_password)

    def test_symbol_password_validator_invalid(self):
        """Test that the password without a symbol fails the validator."""
        invalid_password = "Password123"
        # Assert that a ValidationError is raised.
        with self.assertRaises(ValidationError):
            self.symbol_validator.validate(invalid_password)

    def test_number_password_validator_help_text(self):
        """Test that the help text for the number validator is correct."""
        expected_help_text = "Your password must contain at least 1 digit."
        self.assertEqual(self.number_validator.get_help_text(), expected_help_text)

    def test_uppercase_password_validator_help_text(self):
        """Test that the help text for the uppercase validator is correct."""
        expected_help_text = "Your password must contain at least 1 uppercase letter."
        self.assertEqual(self.uppercase_validator.get_help_text(), expected_help_text)

    def test_lowercase_password_validator_help_text(self):
        """Test that the help text for the lowercase validator is correct."""
        expected_help_text = "Your password must contain at least 1 lowercase letter."
        self.assertEqual(self.lowercase_validator.get_help_text(), expected_help_text)

    def test_symbol_password_validator_help_text(self):
        """Test that the help text for the symbol validator is correct."""
        expected_help_text = "Your password must contain at least 1 symbol."
        self.assertEqual(self.symbol_validator.get_help_text(), expected_help_text)
