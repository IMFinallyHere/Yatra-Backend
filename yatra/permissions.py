from rest_framework.permissions import BasePermission

class CanUpdateActivity(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('yatra.change_activity')

class CanUpdateTrip(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('yatra.change_trip')

class AssignBusToUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('yatra.add_userbus')

class AssignTripToUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('yatra.add_usertrip')