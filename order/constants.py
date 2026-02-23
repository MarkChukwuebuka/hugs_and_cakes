from django.db import models


class OrderType(models.TextChoices):
    dine_in = "Dine In"
    delivery = "Delivery"


class OrderStatus(models.TextChoices):
    completed = "Completed"
    pending = "Pending"
    cancelled = "Cancelled"
    served = "Served"
    confirmed = "Confirmed"
    preparing = "Preparing"

