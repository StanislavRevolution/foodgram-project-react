from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Пользователи"""
    list_display = ('username', 'email')
    list_filter = ('email', 'username')
    search_fields = ('username',)
