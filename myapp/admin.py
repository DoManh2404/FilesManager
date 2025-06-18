from django.contrib import admin

from myapp.models import MyUser

# Register your models here.

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','is_superuser','is_staff','is_active','last_login',)

class MyAdminSite(admin.AdminSite):
    site_header = 'MyApp Admin'

    def each_context(self, request):
        context = super().each_context(request)
        context['site_url'] = '/home/'
        return context

custom_admin_site = MyAdminSite(name='myappadmin')
custom_admin_site.register(MyUser)

admin.site.register(MyUser, PermissionAdmin)