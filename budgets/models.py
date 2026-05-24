from django.db import models

from django.db import models
from core.models import OwnedModel, TimeStampedModel
from categories.models import Category


class Budget(TimeStampedModel, OwnedModel):
    PERIOD_CHOICES = (
        ("monthly", "Monthly"),
        ("weekly", "Weekly"),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)

    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)

    start_date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.limit_amount}"