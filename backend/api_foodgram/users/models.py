from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=150)
    email = models.EmailField('Почта', unique=True)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
