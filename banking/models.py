"""
Banking Models
──────────────
Account  – linked to User, 12-digit unique account number, balance
Transaction – atomic P2P transfer record with idempotency key
"""
import random
from django.db import models
from django.conf import settings


def generate_account_number():
    """Generate a unique 12-digit random account number."""
    while True:
        number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        if not Account.objects.filter(account_number=number).exists():
            return number


class Account(models.Model):
    """Bank Account – one per customer."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='account',
    )
    account_number = models.CharField(
        max_length=12, unique=True, editable=False,
    )
    balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = generate_account_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Account {self.account_number} – {self.user.full_name}'


class TransactionStatus(models.TextChoices):
    SUCCESS = 'SUCCESS', 'Success'
    FAILED = 'FAILED', 'Failed'


class Transaction(models.Model):
    """P2P Transfer record."""

    sender = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='sent_transactions',
    )
    receiver = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='received_transactions',
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=TransactionStatus.choices,
        default=TransactionStatus.SUCCESS,
    )
    idempotency_key = models.CharField(
        max_length=64, unique=True, null=True, blank=True,
        help_text='Unique request key to prevent duplicate transactions.',
    )
    description = models.CharField(max_length=255, blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return (
            f'₹{self.amount} | {self.sender.account_number} → '
            f'{self.receiver.account_number} | {self.status}'
        )
