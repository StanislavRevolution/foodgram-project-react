from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# @api_view(['GET'])
# def get_current_user(request):
#     serializer = UserSerializer(data=request.user, context={'request': request})
#     if serializer.is_valid(raise_exception=True):
#         return Response(serializer.data)
#     return Response(serializer.errors)

