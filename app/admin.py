from django.contrib import admin
from app.models import *

# Register your models here.
# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'email', 'username']

