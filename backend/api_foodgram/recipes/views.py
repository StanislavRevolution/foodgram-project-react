
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import IngredientAmount, Recipe, Tag, Ingredient
from .serializers import (IngredientsSerializer,
                          RecipesGetSerializer,
                          RecipesPostSerializer,
                          TagSerializer,
                          FavoriteSerializer
                          )

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


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
            serializer = FavoriteSerializer(recipe)
            return Response(serializer.data)
        if recipe not in favorites:
            return Response('Такого рецепта нет в избранном!')
        recipe.favorite.remove(request.user)
        return Response('Успешно удалено')

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
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

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        """Создание pdf."""
        # Данные модели
        user = request.user
        template_path = 'pdf.html'
        shop_list = user.shopping_cart_all.all()
        print(shop_list)
        context = {'shop_list': shop_list}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html,
            dest=response,
            encoding='UTF-8'
        )
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer


