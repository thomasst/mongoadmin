from django.contrib import admin
from . import models

class MongoConnectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'host', 'port', 'username']

admin.site.register(models.MongoConnection, MongoConnectionAdmin)
