from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Safe methods like GET are allowed to all authenticated users.
    """

    def has_object_permission(self, request, view, obj):
        # Always allow safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Otherwise, only allow if the object belongs to the user
        return obj.user == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access for unauthenticated users,
    but require login for write operations.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsAdminOrOwner(permissions.BasePermission):
    """
    Admins can access everything. Regular users can only access their own data.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True  # Admin can do anything
        return obj.user == request.user  # Regular user can only access their own stuff


class IsOwner(permissions.BasePermission):
    """
    Only allow access if the request user is the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
