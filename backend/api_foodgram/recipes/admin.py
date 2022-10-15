from django.contrib import admin
from .models import Measure, Ingredient, Tag, Recipe


admin.site.register(Measure)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)

