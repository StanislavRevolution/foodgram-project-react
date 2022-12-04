from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .filters import TagFilter, SearchIngredientFilter
from .models import Ingredient, Recipe, Tag
from .permissions import IsAuthenticatedForPostAndPatch
from .serializers import (FavoriteSerializer, IngredientsSerializer,
                          RecipesGetSerializer, RecipesPostSerializer,
                          TagSerializer)
from .utils import create_user_shopping_cart


class TagsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Обработка тегов для рецептов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('slug', 'name')


class RecipesViewSet(viewsets.ModelViewSet):
    """Создание и обработка рецептов"""
    queryset = Recipe.objects.select_related('author').all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TagFilter
    permission_classes = (IsAuthenticatedForPostAndPatch,)
    ordering = ('-pub_date',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesGetSerializer
        return RecipesPostSerializer

    def get_queryset(self):
        qs = Recipe.objects
        if self.request.query_params.get('is_favorited'):
            qs = qs.filter(favorite__username=self.request.user)
        if self.request.query_params.get('is_in_shopping_cart'):
            qs = qs.filter(shopping_cart__username=self.request.user)
        return qs

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        """Добавление рецептов в избранное"""
        recipe = get_object_or_404(Recipe, pk=pk)
        favorites = request.user.favorite_all.all()
        if request.method == 'POST':
            if recipe in favorites:
                return Response(
                    'Уже добавлено в избранное',
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe.favorite.add(request.user)
            serializer = FavoriteSerializer(recipe)
            return Response(serializer.data)
        if recipe not in favorites:
            return Response(
                'Такого рецепта нет в избранном!',
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe.favorite.remove(request.user)
        return Response('Успешно удалено')

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        """Добавление рецептов в список покупок"""
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_cart = request.user.shopping_cart_all.all()
        if request.method == 'POST':
            serializer = FavoriteSerializer(recipe)
            if recipe in shopping_cart:
                return Response(
                    'Уже добавлено в список покупок!',
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe.shopping_cart.add(request.user)
            return Response(serializer.data)
        if recipe not in shopping_cart:
            return Response('Такого рецепта нет в списке покупок!')
        recipe.shopping_cart.remove(request.user)
        return Response('Успешно удалено')

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Создание pdf."""
        return create_user_shopping_cart(request)


class IngredientsViewSet(viewsets.ModelViewSet):
    """Обработка ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend, SearchIngredientFilter)
    search_fields = ('^name', )
    pagination_class = None
