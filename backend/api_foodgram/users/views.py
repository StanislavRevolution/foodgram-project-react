from django.contrib.auth import get_user_model
from recipes.models import Follow
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SubscribeSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, pk=None):
        author = User.objects.get(pk=pk)
        if request.method == 'POST':
            if request.user == author:
                return Response(
                    'Нельзя подписаться на самого себя',
                    status=status.HTTP_400_BAD_REQUEST
                )
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


class GetAllSubscriptions(APIView, PageNumberPagination):
    def get(self, request):
        user = self.request.user
        queryset = User.objects.filter(following__user=user)
        result = self.paginate_queryset(queryset, request, view=self)
        serializer = SubscribeSerializer(
            result,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)
