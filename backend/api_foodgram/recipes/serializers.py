from django.contrib.auth import get_user_model
from django.db.models import F
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator
from collections import Counter

from users.serializers import UserSerializer

from .models import Ingredient, IngredientAmount, Recipe, Tag
from .filters import TagFilter

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов"""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientsAmountSerializer(serializers.ModelSerializer):
    """Сериализатор для промежуточной таблицы IngredientAmount"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

    def validate(self, data):
        """Проверка времени приготовления"""
        if data['cooking_time'] < 1:
            raise serializers.ValidationError("Cooking_time can't be 0!")
        return data


class RecipesGetSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов при GET запросах"""
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        """Получить ингредиенты, связанные с данным рецептом"""
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit',
            amount=F('ingredient_ammount__amount')
        )

    def get_is_favorited(self, obj):
        """Получить True в случае, если рецепт добавлен в избранное, и False,
        если рецепт отсутствует в избранном пользователя"""
        user = self.context['request'].user
        return (
                user.is_authenticated and
                user.favorite_all.filter(id=obj.id).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Получить True в случае, если рецепт добавлен в список покупок,
         и False, если рецепт отсутствует в списке покупок пользователя"""
        user = self.context['request'].user
        return (
                user.is_authenticated and
                user.shopping_cart_all.filter(id=obj.id).exists()
        )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        filterset_class = TagFilter


class RecipesPostSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов при POST запросах"""
    image = Base64ImageField()
    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientsAmountSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('author', 'name'),
                message='Такой вариант уже создан!'
            )
        ]

    def validate(self, data):
        """Проверка времени приготовления, дубликатов ингредиентов,
        проверка количества, проверка существования тегов"""

        # время приготовления больше 0
        if data['cooking_time'] < 1:
            raise serializers.ValidationError(
                'Неверно указано время приготовления!'
            )
        ings = data['ingredients']
        # проверка на отрицательное количество
        amounts = [(ing.get('id'), ing.get('amount'))
                   for ing in ings
                   if ing.get('amount') < 1]
        if amounts:
            raise serializers.ValidationError(
                f'Неверно указано значение количества для: {dict(amounts)}'
            )
        # проверка дубликатов среди ингредиентов
        titles = [title.get('id') for title in ings]
        duplicates = [k for k, v in Counter(titles).items() if v > 1]
        if duplicates:
            raise serializers.ValidationError(
                f'Указаны дубликаты ингредиентов: {list(duplicates)}'
            )
        # проверка существования тегов в БД
        tags = set(data['tags'])
        for tag in tags:
            if tag not in Tag.objects.all():
                raise serializers.ValidationError(
                    'Такого тега не существует!'
                )
        return data

    def set_user_and_remove_ingredients(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return validated_data.pop('ingredients')

    @transaction.atomic()
    def create(self, validated_data):
        ingredients = self.set_user_and_remove_ingredients(validated_data)
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            ingredient = dict(ingredient)
            IngredientAmount.objects.create(
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount'),
                recipe=recipe
            )
        recipe.tags.set(tags)
        recipe.save()
        return recipe

    @transaction.atomic()
    def update(self, instance, validated_data):
        ingredients = self.set_user_and_remove_ingredients(validated_data)
        instance.tags.set(validated_data.pop('tags'))
        for ingredient in ingredients:
            ingredient = dict(ingredient)
            current_ingredient = get_object_or_404(
                IngredientAmount,
                ingredient=ingredient.get('id'),
                recipe=instance
            )
            current_ingredient.amount = ingredient.get('amount')
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipesGetSerializer(
            instance, context={'request': self.context.get('request')}).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
