from rest_framework import serializers
from .models import User, UserRole


class RegisterSerializer(serializers.ModelSerializer):
    """Public registration – always creates a CUSTOMER."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'full_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            role=UserRole.CUSTOMER,
            **validated_data,
        )


class StaffCreateSerializer(serializers.ModelSerializer):
    """Admin-only – creates a STAFF user."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'full_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            role=UserRole.STAFF,
            is_staff=True,
            **validated_data,
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'full_name', 'role', 'is_active', 'date_joined']
        read_only_fields = fields
