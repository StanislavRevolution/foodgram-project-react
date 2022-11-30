from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

User = settings.AUTH_USER_MODEL


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=300)
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=15
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('Название', max_length=100)
    color = models.CharField('Цветовой HEX-код', max_length=15)
    slug = models.SlugField(max_length=160, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Фото', upload_to="recipes_shots/")
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='ingredient_amount',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(Tag, related_name='tag', verbose_name='Тэг')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        default=0,
        validators=[
            MinValueValidator(1, message='Время приготовления больше 0!')
        ]
    )
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True
    )
    shopping_cart = models.ManyToManyField(
        User,
        related_name='shopping_cart_all',
        verbose_name='Список покупок',
        blank=True
    )
    favorite = models.ManyToManyField(
        User,
        related_name='favorite_all',
        verbose_name='Избранное',
        blank=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'name'),
                name='unique_author_name'
            )
        ]

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Количество'
    )

    class Meta:
        default_related_name = 'ingredient_ammount'
        verbose_name_plural = 'Рецепт-Ингредиент'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_recipe'
            ),
            models.CheckConstraint(
                check=models.Q(amount__gte=1),
                name='amount_gte_1'
            )
        ]

    def __str__(self):
        return f'{self.ingredient.name}: {self.amount}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_user_author'
            )
        ]

    def __str__(self):
        user = self.user
        author = self.author
        return str(user) + " ; " + str(author)
