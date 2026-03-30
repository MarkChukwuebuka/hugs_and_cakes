from django.contrib import admin

from base.admin import BaseAdmin
from order.models import Order, Area, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("total_cost", "original_price", "menu_item", "quantity")
    fields = ("menu_item", "quantity", "original_price", "total_cost")


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = ["order_id", "order_type", "table", "total_amount", "created_by"]
    search_fields = ["order_id", "created_by__email", "status"]
    autocomplete_fields = ("table", "created_by")
    inlines = [OrderItemInline]



@admin.register(Area)
class AreaAdmin(BaseAdmin):
    list_display = ["id", "name", "delivery_fee"]
    list_editable = ["name", "delivery_fee"]