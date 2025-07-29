from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")
    authenticated_user = authenticate(username=email, password=password)

    if authenticated_user:
        token, _ = Token.objects.get_or_create(user=authenticated_user)
        return Response({"valid": True, "token": token.key})
    return Response({"valid": False}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    email = request.data.get("email")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")

    if all([email, password, first_name, last_name]):
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            token = Token.objects.create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
    return Response(
        {"message": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    user = request.user
    return Response(
        {"message": f"Welcome, {user.first_name}! This is a protected endpoint."}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Destroys the user's auth token"""
    try:
        request.user.auth_token.delete()
        return Response(
            {"message": "Logged out successfully."}, status=status.HTTP_200_OK
        )
    except:
        return Response(
            {"message": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST
        )
