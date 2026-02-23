from django.db import models

from base.models import BaseModel
from order.constants import OrderType, OrderStatus
from utils.util import make_order_id


class Order(BaseModel):
    order_id = models.CharField(max_length=100, unique=True, default=make_order_id)
    order_type = models.CharField(max_length=20, choices=OrderType.choices, default=OrderType.delivery)
    table = models.ForeignKey(
        "crm.Table",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )
    delivery_address = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.pending)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.table.number} {self.created_by.email} - order"



class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="items"
    )
    menu_item = models.ForeignKey(
        "crm.MenuItem",
        on_delete=models.SET_NULL,
        null=True
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)  # "No pepper", "Extra spicy"

    def __str__(self):
        return f"{self.order_id} - item"