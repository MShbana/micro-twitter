import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class NumberPasswordValidator:
    def validate(self, password, user=None):
        if not re.findall(r"\d", password):
            raise ValidationError(
                _("The password must contain at least 1 digit."),
                code="password_no_number",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 digit.")


class UpperCasePasswordValidator:
    def validate(self, password, user=None):
        if not re.findall("[A-Z]", password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter."),
                code="password_no_upper",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 uppercase letter.")


class LowerCasePasswordValidator(object):
    def validate(self, password, user=None):
        if not re.findall("[a-z]", password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter."),
                code="password_no_lower",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 lowercase letter.")


class SymbolPasswordValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r"[()[\]{}|\\`~!@#$%^&*_\-+=;:'\",<>./?]", password):
            raise ValidationError(
                _("The password must contain at least 1 symbol."),
                code="password_no_symbol",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 symbol.")