from rest_framework.permissions import BasePermission

class CanUpdateActivity(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('yatra.change_activity')