import uuid

from cloudinary.models import CloudinaryField
from django.db import models

from base.models import BaseModel


# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    cover_image = CloudinaryField(name='images')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            from utils.util import make_slug

            self.code = make_slug(self.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"


class MenuItem(BaseModel):
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="menu_items"
    )
    name = models.CharField(max_length=255, db_index=True)
    slug = models.CharField(max_length=255, db_index=True, unique=True)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    image = CloudinaryField(name="menu_items", blank=True, null=True)

    is_available = models.BooleanField(default=True, db_index=True)
    is_dine_in_available = models.BooleanField(default=True)
    is_delivery_available = models.BooleanField(default=True)

    preparation_time = models.PositiveIntegerField(
        help_text="Preparation time in minutes",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from utils.util import make_slug
            self.slug = make_slug(self.name)
        super().save(*args, **kwargs)


class MenuItemVariation(models.Model):
    menu_item = models.ForeignKey(
        "MenuItem",
        on_delete=models.CASCADE,
        related_name="variations"
    )
    name = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.menu_item.name} - {self.name}"

class AddOn(BaseModel):
    name = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class MenuItemAddOn(BaseModel):
    menu_item = models.ForeignKey(
        "MenuItem",
        on_delete=models.CASCADE,
        related_name="available_addons"
    )
    addon = models.ForeignKey("AddOn", on_delete=models.CASCADE)



class Table(BaseModel):
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.number}"