from django.db import models

from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.code


class ExchangeRate(models.Model):
    base = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="base_rates")
    target = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="target_rates")
    rate = models.DecimalField(max_digits=12, decimal_places=6)
    date = models.DateField()

    class Meta:
        unique_together = ("base", "target", "date")