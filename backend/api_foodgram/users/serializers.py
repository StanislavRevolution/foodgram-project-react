from djoser.serializers import \
    UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

from recipes.models import Follow


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if Follow.objects.filter(user=user, author=obj).exists():
            return True
        return False
