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