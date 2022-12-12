from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    first_name = models.TextField(max_length=150, blank=True)
    last_name = models.TextField(max_length=150, blank=True)
    role = models.CharField(max_length=16, default='user', choices=CHOICES,)
    bio = models.TextField('Биография', blank=True,)
    confirmation_code = models.TextField('Проверочный код', blank=True)

    @property
    def is_user(self):
        if self.role == self.USER:
            return True
        return False

    @property
    def is_moderator(self):
        if self.role == self.MODERATOR:
            return True
        return False

    @property
    def is_admin(self):
        if self.role == self.ADMIN:
            return True
        return False

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        if self.role == 'admin':
            self.is_staff = True
        if self.role == 'user' or self.role == 'moderator':
            self.is_staff = False
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username'],
                name='unique_username'
            ),
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email')
        ]
        ordering = ('role',)
