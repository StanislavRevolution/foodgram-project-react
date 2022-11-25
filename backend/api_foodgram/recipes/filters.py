import django_filters

from recipes.models import Recipe


class TagFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        lookup_expr='contains',
    )
    is_favorited = django_filters.BooleanFilter(
        method='filter_favorite_recipes'
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_shopping_cart'
    )

    def filter_favorite_recipes(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'shopping_cart', 'is_favorited', 'tags', 'is_in_shopping_cart')
