from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdmin, IsStaff, IsCustomer
from core.throttles import OTPRateThrottle

from .models import ActionRequest, ActionStatus, ActionType
from .serializers import (
    CreateActionRequestSerializer,
    ActionRequestSerializer,
    ReviewActionSerializer,
)
from .otp import generate_otp


class CreateActionRequestView(generics.CreateAPIView):

    serializer_class = CreateActionRequestSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def perform_create(self, serializer):
        serializer.save(initiated_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                'message': 'Action request created. Awaiting admin approval.',
                'request': ActionRequestSerializer(serializer.instance).data,
            },
            status=status.HTTP_201_CREATED,
        )


class PendingActionRequestsView(generics.ListAPIView):

    serializer_class = ActionRequestSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return ActionRequest.objects.filter(
            status=ActionStatus.PENDING,
        ).select_related('initiated_by', 'target_account', 'target_account__user')


class ReviewActionRequestView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        try:
            action_request = ActionRequest.objects.select_related(
                'target_account'
            ).get(pk=pk, status=ActionStatus.PENDING)
        except ActionRequest.DoesNotExist:
            return Response(
                {'error': 'Pending action request not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        ser = ReviewActionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        decision = ser.validated_data['action']
        remarks = ser.validated_data.get('admin_remarks', '')

        action_request.reviewed_by = request.user
        action_request.admin_remarks = remarks
        action_request.reviewed_at = timezone.now()

        if decision == 'APPROVE':
            action_request.status = ActionStatus.APPROVED
            self._execute_action(action_request)
        else:
            action_request.status = ActionStatus.REJECTED

        action_request.save()

        return Response({
            'message': f'Action request {decision.lower()}d.',
            'request': ActionRequestSerializer(action_request).data,
        })

    @staticmethod
    def _execute_action(action_request):
        account = action_request.target_account
        if action_request.action_type == ActionType.DEACTIVATE_ACCOUNT:
            account.is_active = False
            account.save(update_fields=['is_active'])
        elif action_request.action_type == ActionType.DELETE_ACCOUNT:
            account.is_active = False
            account.save(update_fields=['is_active'])
        elif action_request.action_type == ActionType.ACTIVATE_ACCOUNT:
            account.is_active = True
            account.save(update_fields=['is_active'])


class AllActionRequestsView(generics.ListAPIView):

    serializer_class = ActionRequestSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = ActionRequest.objects.select_related(
        'initiated_by', 'reviewed_by', 'target_account', 'target_account__user',
    ).all()


class GenerateOTPView(APIView):

    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [OTPRateThrottle]

    def post(self, request):
        code = generate_otp(request.user.id)
        return Response({
            'message': 'OTP generated successfully. Valid for 5 minutes.',
            'otp': code,
        })
