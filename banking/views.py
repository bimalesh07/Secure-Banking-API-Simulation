from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsCustomer, IsStaffOrAdmin
from core.throttles import TransferRateThrottle

from .models import Account, Transaction
from .serializers import (
    AccountSerializer,
    AccountLookupSerializer,
    AccountLookupResponseSerializer,
    TransferSerializer,
    TransactionSerializer,
)
from .services import execute_transfer, TransferError
from security.otp import verify_otp


class MyAccountView(generics.RetrieveAPIView):

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_object(self):
        return self.request.user.account


class AccountListView(generics.ListAPIView):

    queryset = Account.objects.select_related('user').all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]


class AccountLookupView(APIView):

    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        ser = AccountLookupSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        try:
            account = Account.objects.select_related('user').get(
                account_number=ser.validated_data['account_number'],
            )
        except Account.DoesNotExist:
            return Response(
                {'error': 'Account not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            AccountLookupResponseSerializer({
                'account_number': account.account_number,
                'owner_name': account.user.full_name,
                'is_active': account.is_active,
            }).data
        )


class TransferView(APIView):

    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [TransferRateThrottle]

    def post(self, request):
        ser = TransferSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        if not verify_otp(request.user.id, data['otp']):
            return Response(
                {'error': 'Invalid or expired OTP.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            receiver_account = Account.objects.get(
                account_number=data['receiver_account_number'],
            )
        except Account.DoesNotExist:
            return Response(
                {'error': 'Receiver account not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            txn = execute_transfer(
                sender_account=request.user.account,
                receiver_account=receiver_account,
                amount=data['amount'],
                idempotency_key=data.get('idempotency_key'),
                description=data.get('description', ''),
            )
        except TransferError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'message': 'Transfer successful.',
                'transaction': TransactionSerializer(txn).data,
            },
            status=status.HTTP_200_OK,
        )


class TransactionHistoryView(generics.ListAPIView):

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        account = self.request.user.account
        return (
            Transaction.objects
            .filter(sender=account) | Transaction.objects.filter(receiver=account)
        ).order_by('-timestamp')
