from django.contrib import admin
from django_use_email_as_username.admin import BaseUserAdmin
from .models import CustomUser, Social, Education


admin.site.register(CustomUser, BaseUserAdmin)
admin.site.register(Social)
admin.site.register(Education)
