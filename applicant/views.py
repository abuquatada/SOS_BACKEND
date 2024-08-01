from django.shortcuts import render
from rest_framework.response import Response
from applicant.serializers import *
from application.serializers import *
from applicant.models import *
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
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def complete_profile_applicant(request):
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
    serializer=ApplicantSerializer(data=validate_data)
    if serializer.is_valid():
        user = CustomUser.objects.create(**user_data)
        user.set_password(validate_data.get('password'))
        user.save()
        applicant=Applicants.objects.create(
                  id = user,
                  gender = validate_data['gender'],
                  date_of_birth = validate_data['date_of_birth'],
                  phone_number = validate_data['phone_number'],
                  martial_status= validate_data['martial_status'],
                  home_town= validate_data['home_town'],
                  permanent_address= validate_data['permanent_address'],
                  pincode= validate_data['pincode'],
                  current_location= validate_data['current_location'],
                  resume= validate_data['resume'],
                  preferred_job_type=validate_data['preferred_job_type'],
                  preferred_location=validate_data['preferred_location'],
                  availability_to_join=validate_data['availability_to_join'],
                  work_permit_for_USA=validate_data['work_permit_for_USA'],
                  total_years_of_experience=validate_data['total_years_of_experience'],
                  languages=validate_data['languages'],
                  about=validate_data['about']
                )
        
        skills = [int(skills) for skills in request.data.getlist('skills')]
        applicant.skills.add(*skills)
        interested_industry = [int(interested_industry) for interested_industry in request.data.getlist('interested_industry')]
        applicant.interested_industry.add(*interested_industry)
        interested_department = [int(interested_department) for interested_department in request.data.getlist('interested_department')]
        applicant.interested_department.add(*interested_department)
    
        applicant_serializer = ApplicantSerializer(applicant,data = validate_data)
        if applicant_serializer.is_valid():
               applicant_serializer.save()
               
        education_data = {
            'applicant_id': applicant,
            'degree': validate_data.get('degree'),
            'field_of_specialization': validate_data.get('field_of_specialization'),
            'institute_name': validate_data.get('institute_name'),
            'date_of_completion': validate_data.get('date_of_completion'),
        }
        
        industry_obj = Industry.objects.get(industry_id=validate_data.get('industry'))
        department_obj = Department.objects.get(department_id=validate_data.get('department'))
        experience_data = {
            "applicant_id": applicant,
            "company_name": validate_data.get("company_name"),
            "designation": validate_data.get("designation"),
            "description": validate_data.get("description"),
            "department": department_obj,
            "industry": industry_obj,
            "salary": validate_data.get("salary"),
            "start_date": validate_data.get("start_date"),
            "end_date": validate_data.get("end_date"),
        }
        internship_data = {
            "applicant_id": applicant,
            "company_name": validate_data.get("internship_company_name"),
            "position_title": validate_data.get("internship_position_title"),
            "project_name": validate_data.get("internship_project_name"),
            "description": validate_data.get("internship_description"),
            "start_date": validate_data.get("internship_start_date"),
            "end_date": validate_data.get("internship_end_date"),
            "internship_certificate": validate_data.get("internship_certificate"),
        }
        certificate_data = {
            "applicant_id": applicant,
            "certification_name": validate_data.get("certification_name"),
            "issuing_organization": validate_data.get("issuing_organization"),
            "issue_date": validate_data.get("issue_date"),
            "certifcate": validate_data.get("certifcate"),
        }
        experience_obj = ApplicantExperience.objects.create(**experience_data)
        experience_serializer = ApplicantExperienceSerializer(experience_obj)
        education_obj = ApplicantEducation.objects.create(**education_data)
        education_serializer = ApplicantEducationSerializer(education_obj)
        internship_obj = ApplicantInternship.objects.create(**internship_data)
        internship_serializer = ApplicantInternshipSerializer(internship_obj)
        certificate_obj = ApplicantCertification.objects.create(**certificate_data)
        certificate_serializer = ApplicantCertificationSerializer(certificate_obj)

            
        # subject = 'Welcome to YourRecruitmentPortal!'
        # message = f'Thank you {user.first_name} {user.last_name} for registering with YourRecruitmentPortal. We look forward to helping you find your dream job!'
        # sender_email = settings.EMAIL_HOST_USER
        # recipient_list = [user.email]
        # send_mail(subject, message, sender_email, recipient_list)
        return Response(
                    {"message":"user applicant Registered Successfully", "success": True}
               )
    else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET','PATCH', 'DELETE']) 
# @permission_classes([IsAuthenticated])  
def applicant(request, pk=None):
    if request.method == 'GET':
        if pk is not None:
            try:
                profile = Applicants.objects.get(pk=pk)
                serializer = ApplicantSerializer(profile)
                return Response(serializer.data)
            except Applicants.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            profiles = Applicants.objects.all()
            serializer = ApplicantSerializer(profiles, many=True)
            return Response(serializer.data)
        
    
    elif request.method == 'PATCH':
        try:
            applicant_info = Applicants.objects.get(pk=pk)
        except Applicants.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        val_data = request.data
        print('\n\n\n',val_data,'\n\n\n')
        # user_data=val_data.pop('id',{})
        user_data = {
            'first_name': val_data.get('first_name'),
            'last_name': val_data.get('last_name'),
            'email': val_data.get('email'),
        }
        user = applicant_info.id
        user_serializer = UserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()

        serializer = ApplicantSerializer(applicant_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
    
            skills = request.data.getlist("skills")
            if skills:
                skills = [int(skill) for skill in skills]
                print('\n\n\n',skills,'\n\n\n')
                applicant_info.skills.set(skills)
        
            interested_industry = request.data.getlist('interested_industry')
            if interested_industry:
                interested_industry = [int(industry) for industry in interested_industry]
                applicant_info.interested_industry.set(interested_industry)
        
            interested_department = request.data.getlist('interested_department')
            if interested_department:
                interested_department = [int(department) for department in interested_department]
                applicant_info.interested_department.set(interested_department)
            applicant_info.save()
            return Response('Updated successfully')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            applicant = Applicants.objects.get(pk=pk)
        except Applicants.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # applicant.id.delete()
        applicant.delete()
        return Response('Applicant deleted successfully',status=status.HTTP_204_NO_CONTENT)
    


@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def applicant_education(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                applicant_education = ApplicantEducation.objects.get(pk=pk)
                serializer = ApplicantEducationSerializer(applicant_education)
                return Response(serializer.data)
            except ApplicantEducation.DoesNotExist:
                return Response({'Education not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            applicant_educations = ApplicantEducation.objects.all()
            serializer = ApplicantEducationSerializer(applicant_educations, many=True)
            return Response(serializer.data)

    
    elif request.method == 'POST':
        serializer = ApplicantEducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)
        # else:
        return Response('Failed')
    
    elif request.method == 'PATCH':
        try:
            applicant_education = ApplicantEducation.objects.get(pk=pk)
        except ApplicantEducation.DoesNotExist:
            return Response({'Education not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicantEducationSerializer(applicant_education, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            applicant_education = ApplicantEducation.objects.get(pk=pk)
        except ApplicantEducation.DoesNotExist:
            return Response({ 'Education not found'}, status=status.HTTP_404_NOT_FOUND)
        applicant_education.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def applicant_experience(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                applicant_experience = ApplicantExperience.objects.get(pk=pk)
                serializer = ApplicantExperienceSerializer(applicant_experience)
                return Response(serializer.data)
            except ApplicantExperience.DoesNotExist:
                return Response({'Experience not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            applicant_experiences = ApplicantExperience.objects.all()
            serializer = ApplicantExperienceSerializer(applicant_experiences, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ApplicantExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)
        

    elif request.method == 'PATCH':
        try:
            applicant_experience = ApplicantExperience.objects.get(pk=pk)
        except ApplicantExperience.DoesNotExist:
            return Response({'Experience not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicantExperienceSerializer(applicant_experience, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            applicant_experience = ApplicantExperience.objects.get(pk=pk)
        except ApplicantExperience.DoesNotExist:
            return Response({ 'Experience not found'}, status=status.HTTP_404_NOT_FOUND)
        applicant_experience.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)



@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def applicant_internship(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                applicant_internship = ApplicantInternship.objects.get(pk=pk)
                serializer = ApplicantInternshipSerializer(applicant_internship)
                return Response(serializer.data)
            except ApplicantInternship.DoesNotExist:
                return Response({'Certification not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            applicant_internships = ApplicantInternship.objects.all()
            serializer = ApplicantInternshipSerializer(applicant_internships, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ApplicantInternshipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'PATCH':
        try:
            applicant_internship = ApplicantInternship.objects.get(pk=pk)
        except ApplicantInternship.DoesNotExist:
            return Response({'Certification not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicantInternshipSerializer(applicant_internship, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            applicant_internship = ApplicantInternship.objects.get(pk=pk)
        except ApplicantInternship.DoesNotExist:
            return Response({ 'Certification not found'}, status=status.HTTP_404_NOT_FOUND)
        applicant_internship.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)




@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def applicant_certification(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                applicant_certification = ApplicantCertification.objects.get(pk=pk)
                serializer = ApplicantCertificationSerializer(applicant_certification)
                return Response(serializer.data)
            except ApplicantCertification.DoesNotExist:
                return Response({'Certification not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            applicant_certifications = ApplicantCertification.objects.all()
            serializer = ApplicantCertificationSerializer(applicant_certifications, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ApplicantCertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


    elif request.method == 'PATCH':
        try:
            applicant_certification = ApplicantCertification.objects.get(pk=pk)
        except ApplicantCertification.DoesNotExist:
            return Response({'Certification not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicantCertificationSerializer(applicant_certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            applicant_certification = ApplicantCertification.objects.get(pk=pk)
        except ApplicantCertification.DoesNotExist:
            return Response({ 'Certification not found'}, status=status.HTTP_404_NOT_FOUND)
        applicant_certification.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)
    

# @permission_classes([IsAuthenticated])
class FilterApplicantEducation(generics.ListAPIView):
    queryset = ApplicantEducation.objects.all()
    serializer_class =ApplicantEducationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicantEducationFilter

# @permission_classes([IsAuthenticated])
class FilterApplicantExperience(generics.ListAPIView):
    queryset = ApplicantExperience.objects.all()
    serializer_class =ApplicantExperienceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicantExperiencenFilter


# @permission_classes([IsAuthenticated])
class FilterApplicantCertification(generics.ListAPIView):
    queryset = ApplicantCertification.objects.all()
    serializer_class =ApplicantCertificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicantCertificationFilter

# @permission_classes([IsAuthenticated])
class FilterApplicantInternship(generics.ListAPIView):
    queryset = ApplicantInternship.objects.all()
    serializer_class =ApplicantInternshipSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicantInternshipFilter


# @permission_classes([IsAuthenticated])
class FilterApplicant(generics.ListAPIView):    
    queryset = Applicants.objects.all()
    serializer_class =ApplicantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicantFilter

@csrf_exempt
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def SendEmailToSelectedApplicants( request):
        filter_criteria = request.data.get('filter_criteria', {})
        recruiter_email = request.data.get('recruiter_email', 'your@example.com')
        job_link = request.data.get('job_link', 'Link to Job')
        
        selected_applicants = Applicants.objects.filter(**filter_criteria)
        for applicant in selected_applicants:
            send_mail(
                'New Job Opportunity',
                f'Hello {applicant.user_id.first_name}{applicant.user_id.last_name},\nA new job opportunity is available. Check it out at: {job_link} new',
                recruiter_email,
                [applicant.user_id.email],
                fail_silently=False,
            )
        
        return Response({"message": "Emails sent successfully."})

@api_view(['GET'])
def get_applicant_details(request, pk):
    try:
        applicant = Applicants.objects.get(pk=pk)
    except Applicants.DoesNotExist:
        return Response({'error': 'Applicant not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ApplicantSerializer2(applicant)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_applicant(request,pk=None):
    if pk:
        obj = Applicants.objects.get(pk=pk)
        serializers = Applicant_custom(obj)
        return Response(serializers.data)
    else:
        obj = Applicants.objects.all()
        serializers = Applicant_custom(obj,many=True)
        return Response(serializers.data)
    
@csrf_exempt
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_application(request, pk=None,recr_id=None,job_id=None):
    if request.method == 'GET':
        
        if pk:
            try:
                application = Application.objects.filter(applicant_id=pk)
                serializer = Application2Serializer(application,many=True)
                return Response(serializer.data)
            except Application.DoesNotExist:
                return Response({'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        
        elif recr_id:    
            try:
                application = Application.objects.filter(referral_id=recr_id)
                serializer = Application2Serializer(application,many=True)
                return Response(serializer.data)
            except Application.DoesNotExist:
                return Response({'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        elif job_id:    
            try:
                application = Application.objects.filter(job_id=job_id)
                serializer = Application2Serializer(application,many=True)
                return Response(serializer.data)
            except Application.DoesNotExist:
                return Response({'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            applications = Application.objects.all()
            serializer = ApplicationSerializer(applications, many=True)
            return Response(serializer.data) 


@csrf_exempt
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def applicant_with_application(request):
    validate_data = request.data
    print('\n\n\n',validate_data,'\n\n\n')
    role_object=Roles.objects.get(role_id=validate_data['role_id'])
    user_data = {
            'username': validate_data.get('username'),
            'first_name': validate_data.get('first_name'),
            'last_name': validate_data.get('last_name'),
            'email': validate_data.get('email'),
            'role_id': role_object,
            'password': validate_data.get('password'),
        }
    serializer=ApplicantSerializer(data=validate_data)
    if serializer.is_valid():
        user = CustomUser.objects.create(**user_data)
        user.set_password(user_data['password'])
        applicant=Applicants.objects.create(
                  id = user,
                  gender = validate_data['gender'],
                  date_of_birth = validate_data['date_of_birth'],
                  phone_number = validate_data['phone_number'],
                  martial_status= validate_data['martial_status'],
                  home_town= validate_data['home_town'],
                  permanent_address= validate_data['permanent_address'],
                  pincode= validate_data['pincode'],
                  current_location= validate_data['current_location'],
                  resume= validate_data['resume'],
                  preferred_job_type=validate_data['preferred_job_type'],
                  preferred_location=validate_data['preferred_location'],
                  availability_to_join=validate_data['availability_to_join'],
                  work_permit_for_USA=validate_data['work_permit_for_USA'],
                  total_years_of_experience=validate_data['total_years_of_experience'],
                  languages=validate_data['languages'],
                  about=validate_data['about']
                )
        
        skills = [int(skills) for skills in request.data.getlist('skills')]
        applicant.skills.add(*skills)
        interested_industry = [int(interested_industry) for interested_industry in request.data.getlist('interested_industry')]
        applicant.interested_industry.add(*interested_industry)
        interested_department = [int(interested_department) for interested_department in request.data.getlist('interested_department')]
        applicant.interested_department.add(*interested_department)
    
        applicant_serializer = ApplicantSerializer(applicant,data = validate_data)
        if applicant_serializer.is_valid():
               applicant_serializer.save()
               
        education_data = {
            'applicant_id': applicant,
            'degree': validate_data.get('degree'),
            'field_of_specialization': validate_data.get('field_of_specialization'),
            'institute_name': validate_data.get('institute_name'),
            'date_of_completion': validate_data.get('date_of_completion'),
        }
        
        industry_obj = Industry.objects.get(industry_id=validate_data.get('industry'))
        department_obj = Department.objects.get(department_id=validate_data.get('department'))
        experience_data = {
            "applicant_id": applicant,
            "company_name": validate_data.get("company_name"),
            "designation": validate_data.get("designation"),
            "description": validate_data.get("description"),
            "department": department_obj,
            "industry": industry_obj,
            "salary": validate_data.get("salary"),
            "start_date": validate_data.get("start_date"),
            "end_date": validate_data.get("end_date"),
        }
        internship_data = {
            "applicant_id": applicant,
            "company_name": validate_data.get("internship_company_name"),
            "position_title": validate_data.get("internship_position_title"),
            "project_name": validate_data.get("internship_project_name"),
            "description": validate_data.get("internship_description"),
            "start_date": validate_data.get("internship_start_date"),
            "end_date": validate_data.get("internship_end_date"),
            "internship_certificate": validate_data.get("internship_certificate"),
        }
        certificate_data = {
            "applicant_id": applicant,
            "certification_name": validate_data.get("certification_name"),
            "issuing_organization": validate_data.get("issuing_organization"),
            "issue_date": validate_data.get("issue_date"),
            "certifcate": validate_data.get("certifcate"),
        }
        experience_obj = ApplicantExperience.objects.create(**experience_data)
        experience_serializer = ApplicantExperienceSerializer(experience_obj)
        education_obj = ApplicantEducation.objects.create(**education_data)
        education_serializer = ApplicantEducationSerializer(education_obj)
        internship_obj = ApplicantInternship.objects.create(**internship_data)
        internship_serializer = ApplicantInternshipSerializer(internship_obj)
        certificate_obj = ApplicantCertification.objects.create(**certificate_data)
        certificate_serializer = ApplicantCertificationSerializer(certificate_obj)
        
        
        job_object=JobPosting.objects.get(job_id=validate_data.get("job_id"))
        company_object=Company.objects.get(company_id=validate_data.get("company_id"))
        ref_object=Recruiters.objects.get(recruiter_id=validate_data.get("referral_id"))
        applicat_data = {
                "applicant_id": applicant,
                "job_id": job_object,
                "company_id":company_object ,
                "referral_id":ref_object ,
            }
        application_obj = Application.objects.create(**applicat_data)
        ApplicationSerializer(application_obj)
        
        # appli_serializer = ApplicationSerializer(data=application_data)
        # print('\n\n\n',f'this - {appli_serializer}','\n\n\n')
        # if appli_serializer.is_valid():
        #     appli_serializer.save()
        # return Response(appli_serializer.errors)    
            
        # subject = 'Welcome to YourRecruitmentPortal!'
        # message = f'Thank you {user.first_name} {user.last_name} for registering with YourRecruitmentPortal. We look forward to helping you find your dream job!'
        # sender_email = settings.EMAIL_HOST_USER
        # recipient_list = [user.email]
        # send_mail(subject, message, sender_email, recipient_list)
        return Response(
                    {"message":"user applicant Registered Successfully", "success": True}
               )
    else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



@api_view(['GET'])
def ApplicantCount(request, formate=None):
    applicant_count=Applicants.objects.all().values('applicant_id').count()
    print(applicant_count)
    serializers=ApplicantSerializer(applicant_count,many=True).data
    return Response(serializers)