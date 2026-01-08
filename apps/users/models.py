from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password, name=None, dob=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        if not extra_fields.get("is_superuser"):
            if not name or not dob:
                raise ValueError("Name and DOB required for regular users")
        user = self.model(email=email, name=name, dob=dob, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email=email, password=password, name=None, dob=None, **extra_fields)
