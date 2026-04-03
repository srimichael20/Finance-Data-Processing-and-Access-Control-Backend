from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    """
    Permits only Admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class IsAdminOrAnalystReadOnly(permissions.BasePermission):
    """
    Admin has full access. Analyst has read-only access.
    """
    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        
        if request.user.role == 'admin':
            return True
            
        if request.user.role == 'analyst' and request.method in permissions.SAFE_METHODS:
            return True
            
        return False

class DashboardAccessPermission(permissions.BasePermission):
    """
    Dashboard is accessible by Admin, Analyst, and Viewer.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['admin', 'analyst', 'viewer'])
