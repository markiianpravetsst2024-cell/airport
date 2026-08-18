from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            request.user.is_authenticated and
            (obj.user == request.user or getattr(request.user, 'role', None) == 'admin')
        )


class IsFlightNotDeparted(permissions.BasePermission):
    message = "You cannot change your ticket because there are less than 24 hours until departure."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if getattr(request.user, 'role', None) == 'admin' or request.user.is_staff:
            return True
        time_left = obj.flight.departure_time - timezone.now()
        return time_left > timedelta(days=1)