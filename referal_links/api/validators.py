from rest_framework import serializers
import re


def validate_phone_number(value):
    """
    Checks that phone number starts with '+' and followed by numbers.
    """
    phone_pattern = r"^\+\d{1,3}\d{1,14}$"

    if not re.match(phone_pattern, value):
        raise serializers.ValidationError(
            "Invalid phone number."
            "It should start with '+' and followed by numbers."
            "For example: +35976..."
        )


def validate_auth_code(value):
    """
    Checks auth code.
    """
    if not value.isdigit() and len(value) != 4:
        raise serializers.ValidationError(
            "Invalid auth code. "
            "Auth code must contain exactly 4 numbers."
        )


def validate_invite_code(value):
    """
    Checks that provided invite code corresponds pattern and lengh.
    """
    if len(value) != 6:
        raise serializers.ValidationError(
                "Invalid invite code."
            )
    pattern = r"^[+\-/*!&$#?=@<>a-zA-Z0-9]{6}$"
    if not re.match(pattern, value):
        raise serializers.ValidationError(
            "Invalid invite code."
        )
