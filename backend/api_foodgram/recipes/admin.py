from django.contrib import admin
from .models import Measure, Ingredient, Tag, Recipe


admin.site.register(Measure)
admin.site.register(Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("title", "author", "favourite_count")
    list_filter = ('author', 'title', 'tags')
    search_fields = ('title',)

    def favourite_count(self, obj):
        return obj.my_favourite.count()

    favourite_count.short_description = 'Добавлено в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("title", "measure")
    list_filter = ('title',)

