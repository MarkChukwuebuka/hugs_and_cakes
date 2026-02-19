from django.db.models import IntegerChoices, TextChoices


class ActivityType(TextChoices):
    delete = "delete"
    update = "update"
    create = "create"
    approve = "approve"
    reject = "reject"
    revert = "revert"
    activate = "activate"
    verify = "verify"
    deactivate = "deactivate"
    application = "application"
    flag = "flag"
    art_validation = "art_validation"


class ActivityTypeVerb(TextChoices):
    delete = "deleted"
    update = "updated"
    create = "created"
    approve = "approved"
    reject = "rejected"
    revert = "reverted"
    activate = "activated"
    verify = "verified"
    deactivate = "deactivated"
    application = "applied"


class CeleryTaskQueue(TextChoices):
    email = "email"
    logging = "logging"
    default = "default"
    liking = "liking"


class CacheExpiry(IntegerChoices):
    thirty_seconds = 30
    one_minute = 60
    ten_minutes = 600
    five_minutes = 300
    fifteen_minutes = 900
    one_hour = 3600
    one_day = 86400
    one_week = 604800
    one_month = 2592000
    one_year = 31536000
