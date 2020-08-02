from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsAuthorOrParticiations(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):        
        return obj.author == request.user or getattr(obj.expert,'user',None) == request.user\
            or getattr(obj.seller,'user',None) == request.user or getattr(obj.buyer,'user',None) == request.user

class IsParticiations(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj.expert,'user',None) == request.user or getattr(obj.seller,'user',None) == request.user\
            or getattr(obj.buyer,'user',None) == request.user