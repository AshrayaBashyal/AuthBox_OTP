from django.urls import path
from .views import (
    RegisterView, VerifyEmailView, LoginView,
    ForgotPasswordView, ResetPasswordView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-email/", VerifyEmailView.as_view()),
    path("login/", LoginView.as_view()),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
]
