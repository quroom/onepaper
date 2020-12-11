from rest_framework import permissions
from papers.models import Contractor

class IsContractorUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile.user == request.user

class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsAuthorOrParticiations(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        else:
            if request.method in permissions.SAFE_METHODS:
                return Contractor.objects.filter(paper=obj, profile__user=request.user).exists()