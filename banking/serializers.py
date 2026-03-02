from decimal import Decimal
from rest_framework import serializers
from .models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='user.full_name', read_only=True)
    owner_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Account
        fields = [
            'id', 'account_number', 'owner_name', 'owner_email',
            'balance', 'is_active', 'created_at',
        ]
        read_only_fields = fields


class AccountLookupSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=12)


class AccountLookupResponseSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    owner_name = serializers.CharField()
    is_active = serializers.BooleanField()


class TransferSerializer(serializers.Serializer):
    receiver_account_number = serializers.CharField(max_length=12)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=Decimal('0.01'))
    otp = serializers.CharField(max_length=6)
    idempotency_key = serializers.CharField(max_length=64, required=False, default=None)
    description = serializers.CharField(max_length=255, required=False, default='')


class TransactionSerializer(serializers.ModelSerializer):
    sender_account = serializers.CharField(source='sender.account_number')
    receiver_account = serializers.CharField(source='receiver.account_number')

    class Meta:
        model = Transaction
        fields = [
            'id', 'sender_account', 'receiver_account',
            'amount', 'status', 'idempotency_key',
            'description', 'timestamp',
        ]
        read_only_fields = fields
