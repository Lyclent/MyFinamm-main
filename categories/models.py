from django.db import models

from django.db import models
from core.models import OwnedModel


class Category(OwnedModel):
    TYPE_CHOICES = (
        ("income", "Income"),
        ("expense", "Expense"),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )

    def __str__(self):
        return self.name