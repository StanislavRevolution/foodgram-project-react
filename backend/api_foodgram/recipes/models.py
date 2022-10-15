from django.db import models
# from django.contrib.auth import get_user_model
from django.conf import settings


# User = get_user_model()


class Measure(models.Model):
    name = models.CharField("Название", max_length=30, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"


class Ingredient(models.Model):
    title = models.CharField('Название', max_length=300)
    amount = models.PositiveSmallIntegerField(default=0)
    measure = models.ForeignKey(
        Measure,
        related_name='measure_unit',
        verbose_name='Единица измерения',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    title = models.CharField('Название', max_length=100)
    color = models.CharField('Цветовой HEX-код', max_length=15)
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='author',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    title = models.CharField('Название', max_length=500)
    image = models.ImageField('Фото', upload_to="recipes_shots/")
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='all_ingredients',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(Tag, related_name='tag', verbose_name='Тэг')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        default=0
    )
    shop_list = models.BooleanField('Список покупок', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
