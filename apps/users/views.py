from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer, LoginSerializer, OTPVerifySerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer
)
from apps.emails.services import send_verification_email_task, send_reset_password_email_task
from .models import User
from apps.otp.utils import verify_otp



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
