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
            return Contractor.objects.filter(paper=obj, profile__user=request.user).exists()

class IsParticiations(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj.paper.expert,'user',None) == request.user or getattr(obj.paper.seller,'user',None) == request.user\
            or getattr(obj.paper.buyer,'user',None) == request.user

class IsSignatureUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.contractor.profile.user == request.user