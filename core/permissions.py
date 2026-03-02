"""
Custom DRF permissions for RBAC.
"""
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Only ADMIN (Checker) users."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )


class IsStaff(BasePermission):
    """Only STAFF (Maker) users."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'STAFF'
        )


class IsCustomer(BasePermission):
    """Only CUSTOMER users."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'CUSTOMER'
        )


class IsStaffOrAdmin(BasePermission):
    """STAFF or ADMIN users."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('STAFF', 'ADMIN')
        )
