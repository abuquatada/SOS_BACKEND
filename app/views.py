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
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import IntegrityError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



# @permission_classes([IsAuthenticated])     
class User(APIView):  
     def get(self,request):
          users = CustomUser.objects.all()
          serializer = UserSerializer(users, many=True)
          return Response(serializer.data)

@csrf_exempt     
@api_view(['POST'])
def register(request):
    validate_data = request.data
    try:
        user = {
            'username': validate_data.get('username'),
            'first_name': validate_data.get('first_name'),
            'last_name': validate_data.get('last_name'),
            'email': validate_data.get('email'),
            'role_id': validate_data.get('role_id'),
            'password': validate_data.get('password'),
        }
        user_serializer = UserSerializer(data=user)
        if user_serializer.is_valid():
            user_instance = user_serializer.save()
            subject = 'Welcome to YourRecruitmentPortal!'
            message = f'Thank you {user_instance.first_name} {user_instance.last_name} for registering with YourRecruitmentPortal. We look forward to build and grow together!'
            sender_email = settings.EMAIL_HOST_USER
            recipient_list = [user_instance.email]
            send_mail(subject, message, sender_email, recipient_list)
            return Response({"message": "User registered successfully", "success": True})
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError as e:
        if 'unique constraint' in str(e).lower() and 'email' in str(e).lower():
            return Response({"message": "A user with this email already exists.", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "An error occurred while creating the user.", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            login_log = EmployeeLog.objects.create(
                    recruiter_id=user.recruiters.recruiter_id,
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
# @permission_classes([IsAuthenticated])
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