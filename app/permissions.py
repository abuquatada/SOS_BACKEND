from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission

# class IsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role_id.name == 'Admin'
    
# class IsRecruiter(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role_id.name == 'Recruiter'
    
# class IsApplicantReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role_id.name == 'Applicant'
 
class GETPermissions(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.role_id.name == 'Admin':
                return True
            elif user.role_id.name == 'Recruiter':
                if request.method in ['GET']:
                    return True
            elif user.role_id.name == 'Applicant':
                if request.method in ['GET']:
                    return True
        return False    
class GETPOSTPermissions(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.role_id.name == 'Admin':
                return True
            elif user.role_id.name == 'Recruiter':
                if request.method in ['GET','POST']:
                    return True
            elif user.role_id.name == 'Applicant':
                if request.method in ['GET']:
                    return True
        return False    