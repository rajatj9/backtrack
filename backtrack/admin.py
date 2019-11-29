from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'is_developer', 'is_manager', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff')
        })
    )
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'is_developer', 'is_manager', 'password')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff')
        })
    )
    list_display = ['email', 'username', 'is_developer', 'is_manager']
    list_filter = ['is_developer', 'is_manager']
    search_fields = ('email', 'username')
    ordering = ('email',)

# Register your models here.
admin.site.register(PBI)
admin.site.register(Tasks)
admin.site.register(Manager)
admin.site.register(Developer)
admin.site.register(Sprint)
admin.site.register(Project)
admin.site.register(User,UserAdmin)
