from rest_framework import permissions


class HasProfileOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.profiles.exists():
                return True
            else:
                return False
