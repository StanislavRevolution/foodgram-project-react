from django.db import models
from django.contrib.auth.models import AbstractUser

from recipes.models import Recipe


class User(AbstractUser):
    favourite_recipes = models.ManyToManyField(
        Recipe,
        verbose_name='Избранные рецепты',
        related_name='my_favourite',
        blank=True
    )
    subscriptions = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='Подписки на пользователей',
        related_name='all_subscriptions',
        blank=True
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
