from django.contrib import admin

from base.admin import BaseAdmin
from crm.models import MenuItem, Category, Table


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "code"]
    readonly_fields = ["code"]


@admin.register(MenuItem)
class MenuItemAdmin(BaseAdmin):
    list_display = ["id", "name", "base_price", "is_available"]
    search_fields = ["name", "description", "slug"]
    autocomplete_fields = ("category",)



@admin.register(Table)
class TableAdmin(BaseAdmin):
    list_display = ["number", "capacity"]
    search_fields = ["number"]