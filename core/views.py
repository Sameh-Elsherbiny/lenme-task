from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserSerializer,
    LoginSerializer,
    VerifyOtpSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    ChangeEmailSerializer,
    LogoutSerializer,
    DeleteAccountSerializer,
    
)
from rest_framework import serializers
from .models import User
from .utils import Util , create_token
from django.utils.translation import gettext as _


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Util.send_email(user)
        data = {
            "user": serializer.data,
            "message": _("User registered successfully , please verify your Email"),
        }

        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = {
            "user": UserSerializer(serializer.validated_data["user"]).data,
            "token": create_token(serializer.validated_data["user"]),
            "message": _("User logged in successfully"),
        }
        return Response(data, status=status.HTTP_200_OK)


class SendOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            data = {"message": _("User not found")}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        Util.send_email(user=User.objects.get(email=email))
        data = {
            "email": email,
            "message": _("OTP sent successfully , please verify your email"),
        }
        return Response(data, status=status.HTTP_200_OK)


class VerifyOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data.get("new_email"))
        data = {
            "user": UserSerializer(user).data,
            "token": create_token(user),
        }
        response = {"data": data, "message": _("OTP verified successfully")}
        return Response(response, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=serializer.data["email"])
        user_serializer = UserSerializer(user).data
        print(user_serializer)
        data = {
            "user": user_serializer,
            "token": create_token(user),
            }
        response = {"data": data, "message": _("Password reset successfully")}
        return Response(response, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        user = self.request.user
        return user

    def get_serializer_context(self):
        return {"user": self.request.user}

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "user": UserSerializer(request.user).data,
            "token": Token.objects.get_or_create(user=request.user)[0].key,
        }
        response = {"data": data, "message": _("Password changed successfully")}
        return Response(response, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        return user

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteAccountSerializer

    def delete(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        data = {"message": _("Account deleted successfully")}
        return Response(data, status=status.HTTP_200_OK)


class ChangeEmailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "user": UserSerializer(user).data,
            "message": _("Email changed successfully"),
        }
        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"message": _("User logged out successfully")}
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
