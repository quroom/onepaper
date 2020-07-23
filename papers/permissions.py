from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_anonymous

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class Disable(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return False