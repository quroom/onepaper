from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request):
        return request.user.is_staff