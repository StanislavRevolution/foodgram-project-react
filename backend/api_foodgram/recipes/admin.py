from django.contrib import admin

from .models import Follow, Ingredient, IngredientAmount, Recipe, Tag


admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(IngredientAmount)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Рецепты"""
    list_display = ("name", "author", "favourite_count")
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)

    def favourite_count(self, obj):
        return obj.favorite.count()

    favourite_count.short_description = 'Добавлено в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ингредиенты"""
    list_display = ("name", "measurement_unit")
    list_filter = ('name',)
