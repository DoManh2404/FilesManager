from django.contrib import admin
from myapp.models import MyUser, Role


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_superuser', 'is_staff', 'is_active', 'last_login')


class MyAdminSite(admin.AdminSite):
    site_header = 'MyApp Admin'

    def each_context(self, request):
        context = super().each_context(request)
        context['site_url'] = '/home/'
        return context


custom_admin_site = MyAdminSite(name='myapp_admin')  # Không dùng dấu cách

# Đăng ký models vào custom admin
custom_admin_site.register(MyUser, PermissionAdmin)
custom_admin_site.register(Role)
