from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Tag, Recipe, Ingredient
import webcolors
from users.serializers import UserSerializer

User = get_user_model()


class Hex2NameColor(serializers.Field):
    # При чтении данных ничего не меняем - просто возвращаем как есть
    def to_representation(self, value):
        return value

    # При записи код цвета конвертируется в его название
    def to_internal_value(self, data):
        # Доверяй, но проверяй
        try:
            # Если имя цвета существует, то конвертируем код в название
            data = webcolors.hex_to_name(data)
        except ValueError:
            # Иначе возвращаем ошибку
            raise serializers.ValidationError('Для этого цвета нет имени')
        # Возвращаем данные в новом формате
        return data


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'title', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='title')
    measure_unit = serializers.CharField(source='measure')

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measure_unit')

    def validate(self, data):
        """Проверка времени приготовления"""
        if data['cooking_time'] < 1:
            raise serializers.ValidationError("Cooking_time can't be 0!")
        return data

    # def create(self, validated_data):
    #     # Если в исходном запросе не было поля achievements
    #     if 'achievements' not in self.initial_data:
    #         # То создаём запись о котике без его достижений
    #         cat = Cat.objects.create(**validated_data)
    #         return cat
    #
    #     # Иначе делаем следующее:
    #     # Уберём список достижений из словаря validated_data и сохраним его
    #     achievements = validated_data.pop('achievements')
    #     # Сначала добавляем котика в БД
    #     cat = Cat.objects.create(**validated_data)
    #     # А потом добавляем его достижения в БД
    #     for achievement in achievements:
    #         current_achievement, status = Achievement.objects.get_or_create(
    #             **achievement)
    #         # И связываем каждое достижение с этим котиком
    #         AchievementCat.objects.create(
    #             achievement=current_achievement, cat=cat)
    #     return cat


class RecipesSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientsSerializer(many=True, read_only=True)
    name = serializers.CharField(source='title')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )
