from django.db import models
from django.db import models
from core.models import OwnedModel, TimeStampedModel
from accounts.models import Account


class Goal(TimeStampedModel, OwnedModel):
    name = models.CharField(max_length=255)

    target_amount = models.DecimalField(max_digits=14, decimal_places=2)
    current_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name