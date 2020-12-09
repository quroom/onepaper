from rest_framework.permissions import BasePermission, SAFE_METHODS
from profiles.models import Profile, ExpertProfile

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if type(obj) == ExpertProfile:
            return obj.profile.user == request.user
        else:
            return obj.user == request.user

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class IsOwnerOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.designator.user == request.user or obj.designee.user == request.user
        else:
            return obj.designator.user == request.user

class IsProfileUserOrReadonly(BasePermission):
    # def has_permission(self, request, view):id=view.kwargs['pk']
    #     return Profile.objects.filter(id=view.kwargs['pk'], user=request.user).exists()
        
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if type(obj) == ExpertProfile:
            return obj.profile.profile.user == request.user
        else:
            return obj.profile.user == request.user

class IsAuthorOrDesignator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.designator.user == request.user or obj.author==request.user