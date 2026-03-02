from rest_framework import serializers
from .models import ActionRequest


class CreateActionRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionRequest
        fields = ['id', 'action_type', 'target_account', 'reason']

    def validate(self, attrs):
        if ActionRequest.objects.filter(
            target_account=attrs['target_account'],
            action_type=attrs['action_type'],
            status='PENDING',
        ).exists():
            raise serializers.ValidationError(
                'A pending request for this action already exists on this account.'
            )
        return attrs


class ActionRequestSerializer(serializers.ModelSerializer):
    initiated_by_name = serializers.CharField(
        source='initiated_by.full_name', read_only=True,
    )
    reviewed_by_name = serializers.CharField(
        source='reviewed_by.full_name', read_only=True, default=None,
    )
    target_account_number = serializers.CharField(
        source='target_account.account_number', read_only=True,
    )

    class Meta:
        model = ActionRequest
        fields = [
            'id', 'action_type', 'target_account', 'target_account_number',
            'initiated_by', 'initiated_by_name',
            'reviewed_by', 'reviewed_by_name',
            'status', 'reason', 'admin_remarks',
            'created_at', 'reviewed_at',
        ]
        read_only_fields = fields


class ReviewActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['APPROVE', 'REJECT'])
    admin_remarks = serializers.CharField(required=False, default='')
