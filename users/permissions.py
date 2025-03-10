from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to allow only users in the Teachers group.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name="Teachers").exists()
