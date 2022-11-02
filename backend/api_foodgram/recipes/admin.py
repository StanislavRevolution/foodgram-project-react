from django.contrib import admin

from .models import Follow, Ingredient, IngredientAmount, Recipe, Tag

admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(IngredientAmount)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "author")
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)

    # def favourite_count(self, obj):
    #     return obj.my_fav_recipe.count()
    #
    # favourite_count.short_description = 'Добавлено в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "measure_unit")
    list_filter = ('name',)

