from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer, LoginSerializer, OTPVerifySerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer
)
from apps.emails.services import send_verification_email_task, send_reset_password_email_task
from .models import User
from apps.otp.utils import verify_otp
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.otp.tasks import send_otp_email_task



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_verification_email_task.delay(user.id)
        return Response({"msg": "User registered. Check your email for OTP verification."}, status=201)


class VerifyEmailView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        user = User.objects.get(email=email)
        if verify_otp(user.otp_secret, otp):
            user.is_verified = True
            user.otp_secret = None
            user.save()
            return Response({"msg": "Email verified successfully."})
        return Response({"error": "Invalid or expired OTP."}, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=401)
        if not user.is_verified:
            return Response({"error": "Email not verified"}, status=403)
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Prevent email enumeration
            return Response({"msg": "If the email exists, an OTP was sent."})

        if not user.is_verified:
            return Response({"error": "Email not verified"}, status=403)

        send_reset_password_email_task.delay(email)
        return Response({"msg": "OTP sent to your email for password reset."})
