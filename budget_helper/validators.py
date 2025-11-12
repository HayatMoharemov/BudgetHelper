from django.core.exceptions import ValidationError


def username_validator(value: str):
    restricted = 'admin'
    value_lower = value.lower()

    if value_lower == restricted \
        or value_lower.startswith(restricted) \
        or value_lower.endswith(restricted):
        raise ValidationError('Username is already taken')


def password_validator(value: str):

    special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"

    has_letter = any(char.isalpha() for char in value)
    has_digit = any(char.isdigit() for char in value)
    has_special = any(char in special_chars for char in value)

    def validation_error_message():
        raise ValidationError('Password must contain letters, numbers'
                              ' and at least one of the following special characters:'
                              ' ' + special_chars)

    if not has_special:
        validation_error_message()

    if not (has_letter and has_digit):
        validation_error_message()