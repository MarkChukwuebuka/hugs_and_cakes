from django.contrib import admin

from base.admin import BaseAdmin
from order.models import Order, Area


# Register your models here.


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = ["order_id", "order_type", "table", "total_amount", "created_by"]
    search_fields = ["order_id", "created_by__email", "status"]
    autocomplete_fields = ("table", "created_by")



@admin.register(Area)
class AreaAdmin(BaseAdmin):
    list_display = ["id", "name", "delivery_fee"]
    list_editable = ["name", "delivery_fee"]