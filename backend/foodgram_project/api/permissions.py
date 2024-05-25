from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False

        return obj.author == request.user or request.user.role == 'admin'
