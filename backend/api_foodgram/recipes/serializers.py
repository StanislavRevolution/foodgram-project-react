from django.contrib.auth import get_user_model
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from users.serializers import UserSerializer

from .models import Ingredient, IngredientAmount, Recipe, Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов"""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


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
        fields = ('id', 'name', 'measure_unit')

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
            'id', 'name', 'measure_unit',
            amount=F('ingredient_ammount__amount')
        )

    def get_is_favorited(self, obj):
        """Получить True в случае, если рецепт добавлен в избранное, и False,
        если рецепт отсутствует в избранном пользователя"""
        user = self.context['request'].user
        if user.is_authenticated:
            if obj in user.favorite_all.all():
                return True
            return False
        return False

    def get_is_in_shopping_cart(self, obj):
        """Получить True в случае, если рецепт добавлен в список покупок,
         и False, если рецепт отсутствует в списке покупок пользователя"""
        user = self.context['request'].user
        if user.is_authenticated:
            if obj in user.shopping_cart_all.all():
                return True
            return False
        return False

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
        """Проверка времени приготовления, а также существования тэгов в БД"""
        if data['cooking_time'] < 1:
            raise serializers.ValidationError(
                'Неверно указано время приготовления!'
            )
        tags = set(data['tags'])
        for tag in tags:
            if tag not in Tag.objects.all():
                print('Max')
                raise serializers.ValidationError(
                    'Такого тега не существует!'
                )
        return data

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        ingredients = validated_data.pop('ingredients')
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

    def update(self, instance, validated_data):
        validated_data['author'] = self.context['request'].user
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.tags.set(validated_data.pop('tags'))
        ingredients = validated_data.pop('ingredients')
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
