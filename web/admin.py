from django.contrib import admin
from web import models
from web.custom_user_admin import UserAdmin
# Register your models here.

admin.site.register(models.Host)
admin.site.register(models.RemoteUser)
admin.site.register(models.BindHost)
admin.site.register(models.IDC)
admin.site.register(models.HostGroups)
