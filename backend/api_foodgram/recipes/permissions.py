from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAuthenticatedForPostAndPatch(permissions.BasePermission):
    """Доступ для всех при запросах, входящих в SAFE_METHODS, и
     только для автора при POST и PATCH запросах"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
