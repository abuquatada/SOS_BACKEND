from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role_id.name == 'Admin'
    
class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role_id.name == 'Recruiter'
    
class IsApplicantReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role_id.name == 'Applicant'
    
class IsAdminOrRecruiter(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role_id 
            and (request.user.role_id.name == 'Admin' or request.user.role_id.name == 'Recruiter')
        )
        
class IsAdminOrRecruiterOrApplicantReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            
            if request.method == 'GET' and request.user.role_id and request.user.role_id.name == 'Applicant':
                return True
            

            if request.user.role_id and request.user.role_id.name in ['Admin', 'Recruiter']:
                return True

        return False
    
class IsAdminOrReadOnlyForRecruiters(BasePermission):
    """
    Custom permission to allow:
    - Recruiters to only perform GET requests.
    - Admins to perform all operations (GET, POST, PATCH, DELETE).
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.method == 'GET' and request.user.role_id and request.user.role_id.name == 'Recruiter':
              return True
        
            if request.user.role_id and request.user.role_id.name == 'Admin':
              return True
        
        return False