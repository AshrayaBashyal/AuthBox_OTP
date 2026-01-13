from celery import shared_task
from django.core.mail import send_mail
from .utils import generate_otp
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_otp_email_task(email):
    user = User.objects.get(email=email)
    secret, otp = generate_otp()
    user.otp_secret = secret
    user.save()
    send_mail(
        "Your OTP",
        f"Your OTP is: {otp}\nIt is valid for 5 minutes.",
        "no-reply@authbox.com",
        [email],
    )