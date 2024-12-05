import filetype
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from micro_twitter.common import constants

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "profile_picture",
        ]


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "profile_picture",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "validators": [validate_password],
                "style": "password",
            },
            "username": {
                "required": True,
                "allow_blank": False,
            },
        }

    def validate_profile_picture(self, value):
        if not value:
            return

        if value.size > constants.USER_PROFILE_PICTURE_MAX_SIZE_BYTES:
            raise serializers.ValidationError(
                f"Image size cannot exceed {constants.USER_PROFILE_PICTURE_MAX_SIZE_HUMAN_READABLE}."
            )

        file_type = filetype.guess(value)

        if (
            not file_type
            or file_type.extension
            not in constants.USER_PROFILE_PICTURE_ACCEPTED_MIME_TYPES.keys()
            or file_type.mime
            not in constants.USER_PROFILE_PICTURE_ACCEPTED_MIME_TYPES.values()
        ):
            raise serializers.ValidationError(
                f"The allowed formats are {list(constants.USER_PROFILE_PICTURE_ACCEPTED_MIME_TYPES.keys())}."
            )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if value and User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("user with this username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("user with this email already exists.")
        return value


class FollowUserRequestSerializer(serializers.Serializer):
    target_username = serializers.CharField(max_length=50)
