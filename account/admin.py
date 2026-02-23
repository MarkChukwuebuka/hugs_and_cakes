from django.contrib import admin
from django.contrib.auth.models import Group

from account.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "first_name", "last_name"]
    search_fields = ["email", "first_name", "last_name"]

admin.site.unregister(Group)