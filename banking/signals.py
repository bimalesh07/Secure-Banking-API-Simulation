"""
Signal: auto-create an Account whenever a CUSTOMER registers.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Account


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_account_for_customer(sender, instance, created, **kwargs):
    if created and instance.role == 'CUSTOMER':
        Account.objects.create(user=instance)
