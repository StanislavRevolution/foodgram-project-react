import io

from django.db.models import Sum
from django.http import FileResponse
from rest_framework import serializers
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .models import IngredientAmount


def create_user_shopping_cart(request):
    """Создание pdf."""
    shopping_cart = (
        request.user.shopping_cart_all.values(
            'ingredients__name',
            'ingredients__measurement_unit'
        ).annotate(amount=Sum('ingredient_ammount__amount')))
    pdfmetrics.registerFont(TTFont('Arial', 'templates/fonts/arial.ttf'))
    buffer = io.BytesIO()
    canvas1 = canvas.Canvas(buffer)
    canvas1.setLineWidth(.3)
    canvas1.setFont('Arial', 12)
    canvas1.drawString(30, 800, 'Список ваших покупок:')
    canvas1.line(27, 790, 180, 790)
    a = 0
    for recipe in shopping_cart:
        canvas1.drawString(30, 770 - a, str(
            f'Ингредиент: {recipe.get("ingredients__name")}, '
            f'Количество: {recipe.get("amount")}, '
            f'{recipe.get("ingredients__measurement_unit")}'
        ))
        a += 15
    canvas1.line(27, 770 - a, 180, 770 - a)
    canvas1.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


def correct_cooking_time(value):
    if value < 1:
        raise serializers.ValidationError(
            'Время приготовления не может быть меньше 1!'
        )


def set_user_and_remove_ingredients(self, validated_data):
    validated_data['author'] = self.context['request'].user
    return validated_data.pop('ingredients')


def add_ingredient_amount_to_recipe(ingredient, recipe):
    IngredientAmount.objects.get_or_create(
        ingredient=ingredient.get('id'),
        amount=ingredient.get('amount'),
        recipe=recipe
    )
