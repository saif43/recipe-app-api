from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_kwargs):
        """Creates and saves a user"""
        user = self.model(email=self.normalize_email(email), **extra_kwargs)
        user.set_password(password)

        if not email:
            raise ValueError("User must have an email address")

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a superuser"""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model which supports email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

