from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from micro_twitter.users.serializers import (
    FollowUserRequestSerializer,
    RegisterUserSerializer,
)
from micro_twitter.users.tasks import send_email


class RegisterUserAPIView(APIView):
    """Register user."""

    authentication_classes = []
    permission_classes = []
    parser_classes = [
        MultiPartParser,
    ]

    @extend_schema(
        summary="Register user.",
        description="Endpoint to register a user by email, username, password and an optional image.",
        request=RegisterUserSerializer,
        responses={status.HTTP_200_OK: RegisterUserSerializer},
    )
    def post(self, request, *args, **kwargs):
        # Passing the request is needed for retrieving the image full URL.
        serializer = RegisterUserSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_email.apply_async(
            kwargs={
                "subject": "Successful Registration at MicroTwitter",
                "message": "Welcome to MicroTwitter. Your account has been successfully registered.",
                "recipient": serializer.instance.email,
            }
        )
        return Response(serializer.data)


@extend_schema(
    summary="Login user.",
    description="Endpoint to login user, using email and password and return JWT tokens.",
)
class LoginUserAPIView(TokenObtainPairView):
    """Login user using email and password."""


class FollowUserAPIView(APIView):
    """Follow user."""

    @extend_schema(
        summary="Follow user.",
        description="Endpoint to follow user, using target user's username.",
        request=FollowUserRequestSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Successfully followed username123.",
                    }
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "You cannot follow your own account.",
                    }
                },
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "No User matches the given query.",
                    }
                },
            },
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = FollowUserRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_username = serializer.data["target_username"]
        target_user = get_object_or_404(get_user_model(), username=target_username)

        authenticated_user = request.user

        # Prevent self follow.
        if target_user == authenticated_user:
            return Response(
                data={"detail": "You cannot follow your own account."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Prevent unnecessary database checks.
        if not authenticated_user.following.filter(id=target_user.id).exists():
            authenticated_user.following.add(target_user)

        return Response(
            data={"detail": f"Successfully followed {target_user.username}."}
        )
