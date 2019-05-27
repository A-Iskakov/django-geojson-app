from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from backend.models import Provider, ServiceArea


@admin.register(Provider)
class CustomUserAdmin(UserAdmin):
    model = Provider

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'language', 'currency')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    pass
