from django.db import models
from django.conf import settings
from encrypted_fields.fields import EncryptedTextField

class BankConnection(models.Model):
    BANK_CHOICES = [
        ('tinkoff', 'Тинькофф'),
        ('sber', 'Сбер')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=20, choices=BANK_CHOICES)

    access_token = EncryptedTextField()
    refresh_token = EncryptedTextField()
    token_expires_at = models.DateTimeField()
    last_sync = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'bank_name']

    def __str__(self):
        return f"{self.user.email} - {self.get_bank_name_display()}"
    
class Synclog(models.Model):
    connection = models.ForeignKey(BankConnection, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    transactions_found = models.IntegerField(default=0)
    transactions_created = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    def __str__(self):
        return f"Sync {self.connection} at {self.started_at}"