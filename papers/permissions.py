from rest_framework import permissions

from papers.models import Contractor, Signature


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        else:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return False


class IsContractorUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile.user == request.user


class IsSignatureUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.contractor.profile.user == request.user
