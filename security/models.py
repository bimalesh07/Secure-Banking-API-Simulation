from django.db import models
from django.conf import settings


class ActionType(models.TextChoices):
    DEACTIVATE_ACCOUNT = 'DEACTIVATE', 'Deactivate Account'
    DELETE_ACCOUNT = 'DELETE', 'Delete Account'
    ACTIVATE_ACCOUNT = 'ACTIVATE', 'Activate Account'


class ActionStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'


class ActionRequest(models.Model):

    action_type = models.CharField(max_length=20, choices=ActionType.choices)
    target_account = models.ForeignKey(
        'banking.Account',
        on_delete=models.CASCADE,
        related_name='action_requests',
    )
    initiated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='initiated_actions',
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_actions',
    )
    status = models.CharField(
        max_length=10,
        choices=ActionStatus.choices,
        default=ActionStatus.PENDING,
    )
    reason = models.TextField(blank=True, default='')
    admin_remarks = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return (
            f'{self.action_type} on {self.target_account.account_number} '
            f'– {self.status}'
        )
