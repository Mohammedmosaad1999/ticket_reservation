from rest_framework import permissions




class IsAutherOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.auther == request.user
    

class IsAuther(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated