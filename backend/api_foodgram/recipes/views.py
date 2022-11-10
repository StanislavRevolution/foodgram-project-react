import io

from django.db.models import F
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Ingredient, Recipe, Tag
from .permissions import IsAuthenticatedForPostAndPatch
from .serializers import (FavoriteSerializer, IngredientsSerializer,
                          RecipesGetSerializer, RecipesPostSerializer,
                          TagSerializer)


class TagsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Обработка тегов для рецептов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Создание и обработка рецептов"""
    queryset = Recipe.objects.all()
    serializer_class = RecipesPostSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('author', 'shopping_cart', 'favorite', 'tags')
    permission_classes = (IsAuthenticatedForPostAndPatch,)
    ordering = ('-pub_date',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesGetSerializer
        return RecipesPostSerializer

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
                    'Уже добавлено в список покупок',
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
        user = request.user
        shop_list = user.shopping_cart_all.all()
        lst = []
        final = []
        for recipe in shop_list:
            """Создаем список со всеми ингредиентами"""
            ingredients = recipe.ingredients
            lst.append(
                ingredients.values(
                    'name',
                    'measure_unit',
                    amount=F('ingredient_ammount__amount')
                )
            )
        for object in lst:
            """Создаем список со вложенными списками, каждый из которых 
            состоит из названия и количества ингредиента"""
            result = [entry for entry in object]
            for i in range(0, len(result)):
                semi_list = [result[i].get('name'), result[i].get('amount')]
                final.append(semi_list)
        db = {}
        for name, value in final:
            """Формируем словарь с набором данных name:amount, а также
            суммируем значения amount, если ингредиент уже встречался"""
            db[name] = db.get(name, 0) + value
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        buffer = io.BytesIO()
        canvas1 = canvas.Canvas(buffer)
        canvas1.setLineWidth(.3)
        canvas1.setFont('Arial', 12)
        canvas1.drawString(30, 800, 'Список ваших покупок:')
        canvas1.drawString(
            320, 800, 'В foodgram 1.1 появятся единицы измерения,'
        )
        canvas1.drawString(320, 785, 'мы чуть-чуть не успеваем :)')
        canvas1.line(27, 790, 180, 790)
        a = 0
        for ingredient, amount in db.items():
            canvas1.drawString(30, 770 - a, str(f'{ingredient} : {amount}'))
            a += 15
        canvas1.line(27, 770 - a, 180, 770 - a)
        canvas1.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


class IngredientsViewSet(viewsets.ModelViewSet):
    """Обработка ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
