from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import pyotp


User = get_user_model()

def generate_otp(secret=None):
    secret = secret or pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=300)
    return secret, totp.now()


@shared_task
def send_verification_email_task(user_id):
    user = User.objects.get(id=user_id)
    secret, otp = generate_otp()
    user.otp_secret = secret
    user.save()
    send_mail(
        "Verify Your Email",
        f"Your OTP is: {otp}\nIt is valid for 5 minutes.",
        "no-reply@authbox.com",
        [user.email],
    )


@shared_task
def send_reset_password_email_task(email):
    user = User.objects.get(email=email)
    secret, otp = generate_otp()
    user.otp_secret = secret
    user.save()
    send_mail(
        "Reset Your Password",
        f"Your OTP is: {otp}\nIt is valid for 5 minutes.",
        "no-reply@authbox.com",
        [user.email],
    )
