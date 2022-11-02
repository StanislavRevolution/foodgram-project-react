from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import IngredientAmount, Recipe, Tag
from .serializers import (IngredientsSerializer,
                          RecipesGetSerializer,
                          RecipesPostSerializer,
                          TagSerializer,
                          FavoriteSerialzer
                          )


class TagsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesPostSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesGetSerializer
        return RecipesPostSerializer

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        favorites = request.user.favorite_all.all()
        if request.method == 'POST':
            if recipe in favorites:
                return Response({
                    'message': 'Уже добавлено в избранное!',
                    'error': True,
                    'code': 500
                })
            recipe.favorite.add(request.user)
            serializer = FavoriteSerialzer(recipe)
            return Response(serializer.data)
        if recipe not in favorites:
            return Response('Такого рецепта нет в избранном!')
        recipe.favorite.remove(request.user)
        return Response('Успешно удалено')


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientsSerializer


