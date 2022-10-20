from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from recipes.views import TagsViewSet, RecipesViewSet, IngredientsViewSet

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
    # path('users/me/', get_current_user, name='current_user'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
