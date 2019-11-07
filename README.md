# report_system
Django REST api on mongoengine


# Add changes to mongo-auth

1. In mongo-auth/permissions.py add:

       class IsAdminUserOrReadOnly(permissions.BasePermission):
    
           def has_permission(self, request, view):
               SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
               return (request.user['is_staff'] or
                       request.user['is_superuser'] or
                       request.method in SAFE_METHODS)
                     
2. Change mongo-auth/views.py file on one that is stored in auth_view folder.
