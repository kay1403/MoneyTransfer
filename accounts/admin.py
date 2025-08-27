from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'phone_number', 'role', 'is_active', 'is_staff', 'is_kyc_verified')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'is_kyc_verified')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'country')}),
        ('Roles & KYC', {'fields': ('role', 'is_kyc_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone_number', 'country',
                'role', 'is_kyc_verified',
                'password1', 'password2'
            ),
        }),
    )
