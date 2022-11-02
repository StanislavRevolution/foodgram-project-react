from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserSerializer
from recipes.models import Follow

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk=None):
        author = User.objects.get(pk=pk)
        if request.method == 'GET':
            Follow.objects.create(
                user=request.user,
                author=author
            )
            return Response('Подписка создана!')
        subscribe = Follow.objects.get(
                user=request.user,
                author=author
            )
        subscribe.delete()
        return Response('Подписка удалена!')
