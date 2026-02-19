from django.db import models


class OTPIntent(models.TextChoices):
    reset_password = "Reset Password"
    signup = "Signup"



class AccountType(models.TextChoices):
    customer = "Customer"
    admin = "Admin"