from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserSerializer, SubscribeSerializer
from recipes.models import Follow

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk=None):
        author = User.objects.get(pk=pk)
        if request.method == 'POST':
            Follow.objects.create(
                user=request.user,
                author=author
            )
            serializer = SubscribeSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data)
        subscribe = Follow.objects.get(
                user=request.user,
                author=author
            )
        subscribe.delete()
        return Response('Подписка удалена!', status=status.HTTP_204_NO_CONTENT)
