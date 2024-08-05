from django.shortcuts import render
from rest_framework.response import Response
from recruiter.serializers import *
from recruiter.models import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import  settings
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from django.db import IntegrityError
from rest_framework import status


@csrf_exempt
@api_view(['GET', 'POST','PATCH', 'DELETE'])  
# @permission_classes([IsAuthenticated]) 
def recruiter(request, pk=None):
    if request.method == 'GET':
        if pk is not None:
            try:
                profile = Recruiters.objects.get(pk=pk)
                serializer = RecruiterSerializer(profile)
                return Response(serializer.data)
            except Recruiters.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            profiles = Recruiters.objects.all()
            serializer = RecruiterSerializer(profiles, many=True)
            return Response(serializer.data)
        
    
    
    elif request.method == 'PATCH':
        try:
            recruiter_info = Recruiters.objects.get(pk=pk)
        except Recruiters.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        val_data=request.data
        user_data = val_data.pop('user_id',{})
        print('\n\n\n',user_data,'\n\n\n')
        user = recruiter_info.user_id
        print('\n\n\n',user,'\n\n\n')
        user_serializer = UserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        company_data = val_data.pop('companies',[])
        serializer = RecruiterSerializer(recruiter_info, data=val_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated successfully')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':  
        try:
            recruiter = Recruiters.objects.get(pk=pk)
        except Recruiters.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        recruiter.user_id.delete()
        recruiter.delete()
        return Response('Recruiter deleted successfully',status=status.HTTP_204_NO_CONTENT)
    

@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def recruiter_education(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                recruiter_education = RecruiterEducation.objects.get(pk=pk)
                serializer = RecruiterEducationSerializer(recruiter_education)
                return Response(serializer.data)
            except RecruiterEducation.DoesNotExist:
                return Response({'Education not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            recruiter_educations = RecruiterEducation.objects.all()
            serializer = RecruiterEducationSerializer(recruiter_educations, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecruiterEducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)


    elif request.method == 'PATCH':
        try:
            recruiter_education = RecruiterEducation.objects.get(pk=pk)
        except RecruiterEducation.DoesNotExist:
            return Response({'Education not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RecruiterEducationSerializer(recruiter_education, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            recruiter_education = RecruiterEducation.objects.get(pk=pk)
        except RecruiterEducation.DoesNotExist:
            return Response({ 'Education not found'}, status=status.HTTP_404_NOT_FOUND)
        recruiter_education.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def recruiter_experience(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                recruiter_experience = RecruiterExperience.objects.get(pk=pk)
                serializer = RecruiterExperienceSerializer(recruiter_experience)
                return Response(serializer.data)
            except RecruiterExperience.DoesNotExist:
                return Response({'Experience not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            recruiter_experiences = RecruiterExperience.objects.all()
            serializer = RecruiterExperienceSerializer(recruiter_experiences, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecruiterExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)


    elif request.method == 'PATCH':
        try:
            recruiter_experience = RecruiterExperience.objects.get(pk=pk)
        except RecruiterExperience.DoesNotExist:
            return Response({'Experience not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RecruiterExperienceSerializer(recruiter_experience, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            recruiter_experience = RecruiterExperience.objects.get(pk=pk)
        except RecruiterExperience.DoesNotExist:
            return Response({ 'Experience not found'}, status=status.HTTP_404_NOT_FOUND)
        recruiter_experience.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)



@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def recruiter_certification(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                recruiter_certification = RecruiterCertification.objects.get(pk=pk)
                serializer = RecruiterCertificationSerializer(recruiter_certification)
                return Response(serializer.data)
            except RecruiterCertification.DoesNotExist:
                return Response({'Certification not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            recruiter_certifications = RecruiterCertification.objects.all()
            serializer = RecruiterCertificationSerializer(recruiter_certifications, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecruiterCertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)


    elif request.method == 'PATCH':
        try:
            recruiter_certification = RecruiterCertification.objects.get(pk=pk)
        except RecruiterCertification.DoesNotExist:
            return Response({'Certification not found'}, status=status.HTTP_404_NOT_FOUND)
        print('\n\n\n',request.data,'\n\n\n')
        serializer = RecruiterCertificationSerializer(recruiter_certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        print('\n\n\n',serializer.errors,'\n\n\n')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            recruiter_certification = RecruiterCertification.objects.get(pk=pk)
        except RecruiterCertification.DoesNotExist:
            return Response({ 'Certification not found'}, status=status.HTTP_404_NOT_FOUND)
        recruiter_certification.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)
    

@csrf_exempt
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def complete_profile_recruiter(request):
    validate_data = request.data
    print('\n\n\n\n',validate_data,'\n\n\n\n')
    role_object=Roles.objects.get(role_id=validate_data['role_id'])
    user_data = {
            'username': validate_data.get('username'),
            'first_name': validate_data.get('first_name'),
            'last_name': validate_data.get('last_name'),
            'email': validate_data.get('email'),
            'role_id': role_object
        }
    serializer=RecruiterSerializer(data=validate_data)
    if serializer.is_valid():
        user = CustomUser.objects.create(**user_data)
        user.set_password(validate_data.get('password'))
        user.save()
        recruiter=Recruiters.objects.create(
               user_id = user,
               gender = validate_data['gender'],
               date_of_birth = validate_data['date_of_birth'],
               phone_number = validate_data['phone_number'],
               martial_status= validate_data['martial_status'],
               home_town= validate_data['home_town'],
               permanent_address= validate_data['permanent_address'],
               pincode= validate_data['pincode'],
               current_location= validate_data['current_location'],
               resume= validate_data['resume'],
               total_years_of_experience=validate_data['total_years_of_experience'],
               languages=validate_data['languages']
          )
        companies = [int(companies) for companies in request.data.getlist('companies')]
        recruiter.companies.add(*companies)
    
        serializer=RecruiterSerializer(recruiter,data=validate_data)
        if serializer.is_valid():
               serializer.save()
               
        education_data = {
            'recruiter_id': recruiter,
            'degree': validate_data.get('degree'),
            'field_of_specialization': validate_data.get('field_of_specialization'),
            'institute_name': validate_data.get('institute_name'),
            'date_of_completion': validate_data.get('date_of_completion'),
        }
        
        
        experience_data = {
            "recruiter_id": recruiter,
            "company_name": validate_data.get("company_name"),
            "designation": validate_data.get("designation"),
            "description": validate_data.get("description"),
            "salary": validate_data.get("salary"),
            "start_date": validate_data.get("start_date"),
            "end_date": validate_data.get("end_date"),
        }
    
        certificate_data = {
            "recruiter_id": recruiter,
            "certification_name": validate_data.get("certification_name"),
            "issuing_organization": validate_data.get("issuing_organization"),
            "issue_date": validate_data.get("issue_date"),
            "certifcate": validate_data.get("certifcate"),
        }
        experience_obj = RecruiterExperience.objects.create(**experience_data)
        experience_serializer = RecruiterExperienceSerializer(experience_obj)
        education_obj = RecruiterEducation.objects.create(**education_data)
        education_serializer = RecruiterEducationSerializer(education_obj)
        certificate_obj = RecruiterCertification.objects.create(**certificate_data)
        certificate_serializer = RecruiterCertificationSerializer(certificate_obj)       
        # subject = 'Welcome to YourRecruitmentPortal!'
        # message = f'Thank you {user.first_name} {user.last_name} for registering with YourRecruitmentPortal. We are glad to have you on board!'
        # sender_email = settings.EMAIL_HOST_USER
        # recipient_list = [user.email]
        # send_mail(subject, message, sender_email, recipient_list)
        return Response(
                    {"message":"user recruiter Registered Successfully", "success": True}
               )
       
    else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @permission_classes([IsAuthenticated])
class FilterRecruiterEducation(generics.ListAPIView):
    queryset = RecruiterEducation.objects.all()
    serializer_class =RecruiterEducationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecruiterEducationFilter

# @permission_classes([IsAuthenticated])
class FilterRecruiterExperience(generics.ListAPIView):
    queryset = RecruiterExperience.objects.all()
    serializer_class =RecruiterExperienceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecruiterExperiencenFilter


# @permission_classes([IsAuthenticated])
class FilterRecruiterCertification(generics.ListAPIView):
    queryset = RecruiterCertification.objects.all()
    serializer_class =RecruiterCertificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecruiterCertificationFilter

# @permission_classes([IsAuthenticated])
class FilterRecruiter(generics.ListAPIView):
    queryset = Recruiters.objects.all()
    serializer_class =RecruiterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecruiterFilter

@api_view(['GET'])
def get_recruiter_details(request, pk):
    try:
        recruiter = Recruiters.objects.get(pk=pk)
    except Recruiters.DoesNotExist:
        return Response({'error': 'Recruiter not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RecruiterSerializer2(recruiter)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET', 'POST','PATCH', 'DELETE'])  
@permission_classes([IsAuthenticated]) 
def get_recruiter(request, pk=None):
    if request.method == 'GET':
            role = str(request.user.role_id)
            print('\n',role,'\n\n\n')
            if role == 'Recruiter':
                user_id = request.user.recruiters.recruiter_id
                # print('\n\n\n',user_id.recruiters.recruiter_id,'\n\n\n')
                print('\n\n\n',user_id,'\n\n\n')
                try:
                    profile = Recruiters.objects.get(pk=user_id)
                    serializer = Recruiter2Serializer(profile)
                    return Response(serializer.data)
                except Recruiters.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:    
                try:
                    profile = Recruiters.objects.get(pk=pk)
                    serializer = Recruiter2Serializer(profile)
                    return Response(serializer.data)
                except Recruiters.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            

@csrf_exempt
@api_view(['GET', 'POST','PATCH', 'DELETE'])  
# @permission_classes([IsAuthenticated]) 
def get_recruiter_specific(request, pk=None):
    if request.method == 'GET':
            try:
                profile = Recruiter_Specific_Job.objects.filter(recruiter_id=pk)
                serializer = Recruiter_Specific_Job2Serializer(profile,many=True)
                return Response(serializer.data)
            except Recruiter_Specific_Job.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)                               
    
    elif request.method == 'POST':
        data = request.data
        job_ids = data.get('job_id', [])
        recruiter_ids = data.get('recruiter_id', [])
        
        if not job_ids or not recruiter_ids:
            return Response({'error': 'job_id and recruiter_id are required and must be lists'}, status=status.HTTP_400_BAD_REQUEST)
        
        created_jobs = []
        errors = []
        
        for job_id in job_ids:
            for recruiter_id in recruiter_ids:
                job_data = {
                    'job_id': job_id,
                    'recruiter_id': recruiter_id
                }
                print('\n\n\n',job_data,'\n\n\n')
                serializer = Recruiter_Specific_JobSerializer(data=job_data)
                if serializer.is_valid():
                    serializer.save()
                    created_jobs.append(serializer.data)
                else:
                    errors.append(serializer.errors)
        
        if errors:
            return Response({'errors': errors})
        
        return Response({'created_jobs': created_jobs, 'message': 'Jobs assigned successfully'})


@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def emplog(request, pk=None):
    if request.method == 'GET':
       
        if pk:
            try:
                emplog = EmployeeLog.objects.get(pk=pk)
                serializer = EmployeeLogSerializer(emplog)
                return Response(serializer.data)
            except EmployeeLog.DoesNotExist:
                return Response({'employeelog not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            emplogs = EmployeeLog.objects.all().order_by('recruiter_id')
            serializer = EmployeeLogSerializer(emplogs, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        user_id = request.data.get('user')
        activity_type = request.data.get('activity_type')

        if activity_type == 'login':
            try:
                recruiter = Recruiters.objects.get(user_id=user_id)
                login_log = EmployeeLog.objects.create(
                    recruiter_id=recruiter,
                    activity_type='login',
                    remarks='Logged in'
                )
                return Response('Login Recorded Successfully', status=status.HTTP_201_CREATED)
            except Recruiters.DoesNotExist:
                return Response({'Recruiter not found'}, status=status.HTTP_404_NOT_FOUND)

        elif activity_type == 'logout':
            
            try:
                recruiter = Recruiters.objects.get(pk=user_id)
                logout_log = EmployeeLog.objects.create(
                    recruiter_id=recruiter,
                    activity_type='logout',
                    remarks='Logged out'
                )
                total_work_hours = logout_log.total_work_hours()
                return Response({
                    'message': 'Logout Recorded Successfully',
                    'total_work_hours': total_work_hours
                }, status=status.HTTP_201_CREATED)
            except Recruiters.DoesNotExist:
                return Response({'Recruiter not found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'Invalid activity type'}, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'PATCH':
        try:
            emplog = EmployeeLog.objects.get(pk=pk)
        except EmployeeLog.DoesNotExist:
            return Response({'EmployeeLog not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeLogSerializer(emplog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            emplog = EmployeeLog.objects.get(pk=pk)
        except EmployeeLog.DoesNotExist:
            return Response({ 'EmployeeLog not found'}, status=status.HTTP_404_NOT_FOUND)
        emplog.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)

class FilterEmplog(generics.ListAPIView):    
    queryset = EmployeeLog.objects.all()
    serializer_class =EmployeeLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeLogFilter




