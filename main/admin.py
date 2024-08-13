from django.contrib import admin
from .models import Patient, Feedback, Polls, Answer
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        if not change:  
            obj.username = obj.email
        super().save_model(request, obj, form, change)


class CustomAdminSite(admin.AdminSite):
    site_header = 'Mental Health Support Community'
    site_title = 'MHSC Admin'
    index_title = 'Welcome to the MHSC Admin Panel'


# Instantiate the custom admin site
custom_admin_site = CustomAdminSite(name='customadmin')

# Register the models with the custom admin site
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Patient)
custom_admin_site.register(Feedback)
custom_admin_site.register(Polls)
custom_admin_site.register(Answer)
