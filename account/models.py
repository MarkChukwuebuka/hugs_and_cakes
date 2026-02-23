from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from base.models import AppDbModel, BaseModel


class OtpBase(AppDbModel):
    otp = models.CharField(max_length=255, null=False)
    otp_requested_at = models.DateTimeField(null=False)
    is_otp_verified = models.BooleanField(default=False)
    otp_verified_at = models.DateTimeField(null=True)
    trials = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Otp(OtpBase):
    user = models.OneToOneField("account.User", on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.email


class User(AbstractUser, BaseModel):
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=50, db_index=True, null=True, unique=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(f"{self.email}")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    groups = None
    user_permissions = None



class ApiRequestLogger(AppDbModel):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, null=True, related_name="+")
    path = models.CharField(max_length=255)
    ref_id = models.CharField(null=False, db_index=True, max_length=255)
    headers = models.JSONField(default=dict)
    request_data = models.JSONField(null=True, blank=True)
    response_body = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "API Request Logs"
