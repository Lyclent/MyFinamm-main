from django.db import models
from django.db import models
from core.models import OwnedModel, TimeStampedModel


class Notification(TimeStampedModel, OwnedModel):
    TYPE_CHOICES = (
        ("budget", "Budget limit"),
        ("subscription", "Subscription"),
        ("system", "System"),
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    title = models.CharField(max_length=255)
    message = models.TextField()

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title