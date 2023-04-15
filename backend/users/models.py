from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name="Подписчик"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name="Автор рецепта"
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='double_follow'
            ),
            CheckConstraint(
                name='self_follow',
                check=~models.Q(user=models.F('author')),
            ),
        ]

    def clean(self):
        if self.user == self.author:
            raise ValidationError('you cannot follow yourself')

    def __str__(self) -> str:
        return str(f'{self.user} подписан на {self.author}')
