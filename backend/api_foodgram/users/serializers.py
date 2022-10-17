from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer
)
from .models import CustomUser


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
