from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Employee, ProjectManager, HR


admin.site.site_header = "HR System Admin"
admin.site.site_title = "HR System Admin Portal"
admin.site.index_title = "Welcome to HR System Portal"

# Customizing UserAdmin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Roles and Permissions', {'fields': ('role', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'email', 'first_name', 'last_name'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register User, Employee, ProjectManager, and HR models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Employee)
admin.site.register(ProjectManager)
admin.site.register(HR)