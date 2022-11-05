from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import IngredientsViewSet, RecipesViewSet, TagsViewSet
from users.views import UserViewSet

app_name = 'api'

router = DefaultRouter()

router.register('users', UserViewSet, basename='user'),
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
# router.register(r'recipes/(?P<id>\d+)/favorite', FavoriteViewSet, basename='favorite')
# router.register(r'recipes/(?P<id>\d+)/shopping_cart', ShoppingCartViewSet, basename='shopping-cart')
# router.register(r'users/subscriptions', SubscriptionViewSet, basename='subscription')
# router.register(r'users/(?P<id>\d+)/subscribe', SubscribeUnsubscribeViewSet, basename='subscribe')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
