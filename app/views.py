from django.shortcuts import render
from rest_framework.response import Response
from app.serializers import *
from recruiter.serializers import *
from app.models import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import  settings
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import IntegrityError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password



# @permission_classes([OnlyAdmin])
class User(APIView):
    def get(self,request):
          users = CustomUser.objects.all()
          serializer = UserSerializer(users, many=True)
          return Response(serializer.data)
    
    def post(self,request):
        validate_data = request.data
        print('\n\n\n',validate_data,'\n\n\n')
        role_object=Roles.objects.get(role_id=validate_data['role_id'])
        user_data = {
                'username': validate_data.get('username'),
                'first_name': validate_data.get('first_name'),
                'last_name': validate_data.get('last_name'),
                'email': validate_data.get('email'),
                'role_id': role_object
            }
        serializer=UserSerializer(data=validate_data)
        if serializer.is_valid():
            user = CustomUser.objects.create(**user_data)
            user.set_password(validate_data.get('password'))
            user.save()
            return Response(
                        {"message":"user applicant Registered Successfully", "success": True}
                   )
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    print('\n\n\n',user,'\n\n\n')
    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        user_role =str(user.role_id)
        print('\n\n\n',user_role,'\n\n\n')
        if user_role == 'Recruiter':
            access_token['recruiter_id']=user.recruiters.recruiter_id
            recruiter_instance = Recruiters.objects.get(recruiter_id=user.recruiters.recruiter_id)
            login_log = EmployeeLog.objects.create(
                    recruiter_id=recruiter_instance,
                    activity_type='login',
                    remarks='Logged in'
                )
            print('\n\n\n',f'this is recruiter {user.recruiters.recruiter_id}','\n\n\n')
        elif user_role == 'Applicant':
            access_token['applicant_id']=user.applicants.applicant_id
            print('\n\n\n',f'this is applicant {user.applicants.applicant_id}','\n\n\n') 
        else :
            print('\n\n\n',None,'\n\n\n')    
        access_token['role']=user_role
        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([GETPermissions])
def roles(request, pk=None):
    if request.method == 'GET':
        if pk is not None:
            try:
                role = Roles.objects.get(pk=pk)
                serializer = RoleSerializer(role)
                return Response(serializer.data)
            except Roles.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            roles = Roles.objects.all()
            serializer = RoleSerializer(roles, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Role added successfully', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            role = Roles.objects.get(pk=pk)
        except Roles.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Role updated successfully')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            role = Roles.objects.get(pk=pk)
        except Roles.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        role.delete()
        return Response('Role deleted successfully',status=status.HTTP_204_NO_CONTENT)




class Logout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        role = str(request.user.role_id)
        if role == 'Recruiter':
            user_id = request.user.recruiters.recruiter_id
            recruiter = Recruiters.objects.get(pk=user_id)
            logout_log = EmployeeLog.objects.create(
                    recruiter_id=recruiter,
                    activity_type='logout',
                    remarks='Logged out'
                )   
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"Message":"Enter refresh_token"})
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"Success"},
                            status=status.HTTP_200_OK
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
        
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].strip().lower()
            try:
                user = CustomUser.objects.get(email__iexact=email) 
            except user.DoesNotExist:
                return Response({"error": "user with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            token = PasswordResetTokenGenerator().make_token(user)
            base_url = request.build_absolute_uri('/')[:-1]
            reset_url = f"{base_url}/passwordresetconfirm/{user.id}/{token}/"
            sender_email = settings.EMAIL_HOST_USER
            recipient_email = user.email
            try:
                send_mail(
                    'Password Reset Request',
                    f'Hi {user.username},\nUse the link below to reset your password:\n{reset_url}',
                    sender_email,
                    [recipient_email],
                    
                )
            except Exception as e:
                return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"message": "Password reset link sent", "reset_url": reset_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetConfirmView(APIView):
    def post(self,request,token,id):
        print(f"Received ID--{id}-----token---{token}")
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['newpassword']
            try:
                user = CustomUser.objects.get(pk=id)
                if PasswordResetTokenGenerator().check_token(user,token):
                    user.set_password(password)
                    user.save()
                    return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            print(user)
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if not check_password(old_password, user.password):
                return Response({"message":"Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
            
            return Response({"detail": "Password has been changed successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)