import django_filters
from recipes.models import Recipe


class TagFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        lookup_expr='contains',
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'shopping_cart',
            'tags'
        )
