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
    delivery_address = models.ForeignKey("DeliveryAddress", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.pending)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.order_id} - order"



class OrderItem(BaseModel):
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
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.order.order_id} - {self.menu_item}"


class DeliveryAddress(BaseModel):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    area = models.ForeignKey("Area", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.email} - delivery address"


class Area(models.Model):
    name = models.CharField(max_length=100)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name