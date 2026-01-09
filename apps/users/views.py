from rest_framework.views import APIView
from .serializers import (
    RegisterSerializer)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_verification_email_task.delay(user.id)
        return Response({"msg": "User registered. Check your email for OTP verification."}, status=201)
