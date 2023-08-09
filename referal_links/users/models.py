from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user model manager where phone_number is the unique identifier
    for authentication instead of username.
    """
    def create_user(self, phone_number, password=None, **extra_fields):
        user = self.model(phone_number=phone_number,
                          password=None,
                          **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Creates Superuser with phone_number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        user = self.create_user(phone_number, password, **extra_fields)
        return user


class User(AbstractUser):
    """Keeps informations about user."""
    phone_number = models.CharField(
        verbose_name='phone_number',
        max_length=20,
        unique=True
    )
    auth_code = models.CharField(
        verbose_name='code for authentication',
        max_length=4,
        null=True
    )
    invite_code = models.CharField(
        verbose_name='invitation code',
        max_length=6,
        null=True
    )
    activated_invite_code = models.CharField(
        verbose_name='other invitation code',
        max_length=6,
        null=True,
        blank=True
    )
    username = models.CharField(
        verbose_name='username',
        max_length=30,
        null=True,
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    class Meta:
        ordering = ["-date_joined"]


class Invite(models.Model):
    """Keeps information about users keeping invitations."""

    invitation_belong_to = models.ForeignKey(User,
                                             related_name='invited_users',
                                             on_delete=models.CASCADE)
    invited_user = models.ForeignKey(User,
                                     related_name='invitations',
                                     on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.invited_user}'
