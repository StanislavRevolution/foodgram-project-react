from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Measure(models.Model):
    name = models.CharField("Название", max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=300)
    amount = models.PositiveSmallIntegerField(default=0)
    measure = models.ManyToManyField(
        Measure,
        related_name='measure_unit',
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.CharField('Название', max_length=100)
    hex = models.CharField('Цветовой HEX-код', max_length=15)
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    title = models.CharField('Название', max_length=500)
    image = models.ImageField('Фото', upload_to="recipes_shots/")
    description = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='all_ingredients',
        verbose_name='Ингредиенты'
    )
    tag = models.ManyToManyField(Tag, related_name='tag', verbose_name='Тэг')
    time = models.PositiveSmallIntegerField('Время приготовления', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
