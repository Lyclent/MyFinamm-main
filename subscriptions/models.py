from django.db import models
from django.db import models
from core.models import OwnedModel, TimeStampedModel
from categories.models import Category
from accounts.models import Account


class Subscription(TimeStampedModel, OwnedModel):
    PERIOD_CHOICES = (
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    )

    name = models.CharField(max_length=255)

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)

    next_payment_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name