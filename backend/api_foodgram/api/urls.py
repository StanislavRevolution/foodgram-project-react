from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from recipes.views import IngredientsViewSet, RecipesViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter
from users.views import GetAllSubscriptions, UserViewSet

app_name = 'api'

router = DefaultRouter()

router.register('users', UserViewSet, basename='subscription')
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')


urlpatterns = [
    path(
        'users/subscriptions/',
        GetAllSubscriptions.as_view(),
        name='all_subscriptions'
    ),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
