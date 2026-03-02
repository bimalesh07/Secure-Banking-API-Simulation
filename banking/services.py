"""
Core transfer logic with:
  • transaction.atomic()
  • select_for_update()  (Pessimistic Locking)
  • Idempotency check
"""
from decimal import Decimal
from django.db import transaction

from .models import Account, Transaction, TransactionStatus


class TransferError(Exception):
    """Raised when a transfer cannot be completed."""
    pass


def execute_transfer(
    sender_account: Account,
    receiver_account: Account,
    amount: Decimal,
    idempotency_key: str | None = None,
    description: str = '',
) -> Transaction:
    """
    Execute an atomic P2P money transfer.

    Uses select_for_update to acquire row-level locks on both accounts
    (ordered by PK to avoid deadlocks) before modifying balances.
    """

    if amount <= 0:
        raise TransferError('Transfer amount must be positive.')

    if sender_account.pk == receiver_account.pk:
        raise TransferError('Cannot transfer to the same account.')

    # ── Idempotency: return existing txn if key already used ────────────
    if idempotency_key:
        existing = Transaction.objects.filter(
            idempotency_key=idempotency_key
        ).first()
        if existing:
            return existing

    # ── Atomic block with pessimistic locks ─────────────────────────────
    with transaction.atomic():
        # Lock rows in consistent order (by PK) to prevent deadlocks
        pks = sorted([sender_account.pk, receiver_account.pk])
        locked = list(
            Account.objects.filter(pk__in=pks)
            .select_for_update()
            .order_by('pk')
        )

        # Re-map to sender / receiver after locking
        locked_map = {a.pk: a for a in locked}
        sender = locked_map[sender_account.pk]
        receiver = locked_map[receiver_account.pk]

        # Validate
        if not sender.is_active:
            raise TransferError('Sender account is deactivated.')
        if not receiver.is_active:
            raise TransferError('Receiver account is deactivated.')
        if sender.balance < amount:
            raise TransferError('Insufficient balance.')

        # Debit & Credit
        sender.balance -= amount
        receiver.balance += amount
        sender.save(update_fields=['balance', 'updated_at'])
        receiver.save(update_fields=['balance', 'updated_at'])

        # Record transaction
        txn = Transaction.objects.create(
            sender=sender,
            receiver=receiver,
            amount=amount,
            status=TransactionStatus.SUCCESS,
            idempotency_key=idempotency_key,
            description=description,
        )

    return txn
