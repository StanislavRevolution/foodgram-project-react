from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer
)
from rest_framework import serializers

from recipes.models import Follow, Recipe

User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    """Сериализатор для регистрации пользователей"""
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных о пользователе"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Получить True в случае, если пользователь подписан на данного
         автора, и False, если подписка отсутствует"""
        user = self.context['request'].user
        if user.is_authenticated:
            if Follow.objects.filter(user=user, author=obj).exists():
                return True
            return False
        return False


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов, который
     является вложенным в SubscribeSerializer"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок на пользователей"""
    recipes = RecipeShortSerializer(many=True, source='author')
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        """Получить True в случае, если пользователь подписан на данного
         автора, и False, если подписка отсутствует"""
        user = self.context['request'].user
        if user.is_authenticated:
            if Follow.objects.filter(user=user, author=obj).exists():
                return True
            return False
        return False

    def get_recipes_count(self, obj):
        """Получить количество рецептов, созданных пользователем"""
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.author.all().count()
        return 0

