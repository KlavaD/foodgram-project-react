from django.contrib.auth.models import AbstractUser
from django.db import models

from backend.settings import FIELD_EMAIL_LENGTH, NAMES_LENGTH
from users.validators import username_validator


class User(AbstractUser):
    email = models.EmailField(
        max_length=FIELD_EMAIL_LENGTH,
        unique=True,
        verbose_name='Электронная почта'
    )

    username = models.CharField(
        max_length=NAMES_LENGTH,
        unique=True,
        validators=[username_validator],
        verbose_name='Никнейм'
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    USERNAME_FIELDS = 'email'

    def __str__(self):
        return self.username
