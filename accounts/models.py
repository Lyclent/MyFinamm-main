from django.db import models
from django.db import models
from core.models import TimeStampedModel, OwnedModel
from currency.models import Currency


class Account(TimeStampedModel, OwnedModel):
    ACCOUNT_TYPES = (
        ("cash", "Cash"),
        ("card", "Card"),
        ("bank", "Bank"),
        ("crypto", "Crypto"),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.balance})"