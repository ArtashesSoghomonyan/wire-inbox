from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return not request.user or not request.user.is_authenticated


class IsVerified(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_verified)
