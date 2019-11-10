# report_system
Django REST api on mongoengine

### Run project

1. python 3.7

2. Create and activate venv 

3. Clone repositoty and install requirements

4. Create file secret_info.py in root directory and add secret info (see in settings.py)

### Add changes to mongo-auth module (venv/lib/python3.7/site-packages/mongo-auth)

1. In mongo-auth/permissions.py add:

       class IsUserAdminOrReadOnly(permissions.BasePermission):
    
           def has_permission(self, request, view):
               SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
               return (request.user['is_staff'] or
                       request.user['is_superuser'] or
                       request.method in SAFE_METHODS)
                       
       class IsUserAdmin(permissions.BasePermission):

           def has_permission(self, request, view):
               return request.user['is_staff'] or request.user['is_superuser']
               
                     
2. Change mongo-auth/views.py and mongo-auth/db.py files on ones that are stored in mango_auth_files_to_change folder.
