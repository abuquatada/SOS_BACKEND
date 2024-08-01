from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role_id and request.user.role_id.name =="Admin":
            if request.method in ['GET','POST']:
                return True
        return False
    
    
class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role_id and request.user.role_id.name == "Recruiter":
            if request.method in ['GET', 'POST']:
                return True
        return False
            
    
class IsApplicant(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_authenticated and request.user.role.name =="Applicant"