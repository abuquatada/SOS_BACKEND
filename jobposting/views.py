from django.shortcuts import render
from rest_framework.response import Response
from jobposting.serializers import *
from jobposting.models import *
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
from applicant.models import Applicants
from rest_framework.parsers import MultiPartParser, FormParser
import csv
from django.utils import timezone

@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def jobstatus(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                job_status = JobStatus.objects.get(pk=pk)
                serializer = JobStatusSerializer(job_status)
                return Response(serializer.data)
            except JobStatus.DoesNotExist:
                return Response({'JobStatus not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            job_statuses = JobStatus.objects.all()
            serializer = JobStatusSerializer(job_statuses, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        user_id = request.data.get('user')
        job_status_data = {**request.data, 'user': user_id}
        job_status_serializer = JobStatusSerializer(data=job_status_data)
    
        if job_status_serializer.is_valid():
            job_status_serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)
        return Response(job_status_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'PATCH':
        try:
            job_status = JobStatus.objects.get(pk=pk)
        except JobStatus.DoesNotExist:
            return Response({'JobStatus not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobStatusSerializer(job_status, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            job_status = JobStatus.objects.get(pk=pk)
        except JobStatus.DoesNotExist:
            return Response({ 'JobStatus not found'}, status=status.HTTP_404_NOT_FOUND)
        job_status.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def jobposting(request, pk=None):
    if request.method == 'GET':
        
        start_date=timezone.now() - timezone.timedelta(days=30)
        end_date=timezone.now()
        count=JobPosting.objects.filter(created_at__range=[start_date,end_date]).count()
        
        if 'count' in request.query_params:
            return Response({'jobpost_count':count})
    
        if pk:
            try:
                jobposting = JobPosting.objects.get(pk=pk)
                serializer = JobPostingSerializer(jobposting)
                return Response(serializer.data)
            except JobPosting.DoesNotExist:
                return Response({'JobPosting not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            jobpostings = JobPosting.objects.all()
            serializer = JobPostingSerializer(jobpostings, many=True)
            return Response(serializer.data)


    elif request.method == 'POST':
        
        print('\n\n\n',request.data,'\n\n\n')
        serializer = JobPostingSerializer(data=request.data)
        if serializer.is_valid():
            jobpost_data = serializer.save()
            company_id = request.data.get('company')
            company_data = None

            if company_id:
                try:
                    company_instance = Company.objects.get(pk=company_id)
                    company_data = CompanySerializer2(company_instance).data
                except Company.DoesNotExist:
                    return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

            skills_data = request.data.get('skills', [])
            if skills_data:
                jobpost_data.skills.set(skills_data)
            matching_applicants = Applicants.objects.filter(skills__in=skills_data)

            for applicant in matching_applicants:
                send_mail(
                    'New Job Opportunity',
                    f'Hello {applicant.id.first_name} {applicant.id.last_name},\nA new job matching your skills has been posted. Check it out at: [Link to Job]',
                    'your@example.com',  
                    [applicant.id.email],
                    fail_silently=False,
                )

            response_data = serializer.data
            if company_data:
                response_data.update({'company': company_data})
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    elif request.method == 'PATCH':
        try:
            jobposting = JobPosting.objects.get(pk=pk)
        except JobPosting.DoesNotExist:
            return Response({'JobPosting not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobPostingSerializer(jobposting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            skills_data = request.data.get('skills', [])
            if skills_data:
                jobposting.skills.set(skills_data)

            return Response('Updated Successfully')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            jobposting = JobPosting.objects.get(pk=pk)
        except JobPosting.DoesNotExist:
            return Response({'JobPosting not found'}, status=status.HTTP_404_NOT_FOUND)
        jobposting.delete()
        return Response('Deleted Successfully', status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def jobstatuslog(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                jobstatuslog = JobStatusLog.objects.get(pk=pk)
                serializer = JobStatusLogSerializer(jobstatuslog)
                return Response(serializer.data)
            except JobStatusLog.DoesNotExist:
                return Response({'JobStatusLog not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            jobstatuslogs = JobStatusLog.objects.all()
            serializer = JobStatusLogSerializer(jobstatuslogs, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        user_id = request.data.get('user')
        jobstatuslog_data = {**request.data, 'user': user_id}
        jobstatuslog_serializer = JobStatusLogSerializer(data=jobstatuslog_data)
    
        if jobstatuslog_serializer.is_valid():
            jobstatuslog_serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)
        return Response(jobstatuslog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'PATCH':
        try:
            jobstatuslog = JobStatusLog.objects.get(pk=pk)
        except JobStatusLog.DoesNotExist:
            return Response({'JobStatusLog not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobStatusLogSerializer(jobstatuslog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            jobstatuslog = JobStatusLog.objects.get(pk=pk)
        except JobStatusLog.DoesNotExist:
            return Response({ 'JobStatusLog not found'}, status=status.HTTP_404_NOT_FOUND)
        jobstatuslog.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)
    
# @permission_classes([IsAuthenticated])
class FilterJobPosting(generics.ListAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobPostingFilter


# @permission_classes([IsAuthenticated])
class FilterJobStatusLog(generics.ListAPIView):
    queryset = JobStatusLog.objects.all()
    serializer_class = JobStatusLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobStatusLogFilter


@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def industry(request, pk=None):
    if request.method == 'GET':
        if pk is not None:
            try:
                industry = Industry.objects.get(pk=pk)
                serializer = IndustrySerializer(industry)
                return Response(serializer.data)
            except Industry.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            industries = Industry.objects.all()
            serializer = IndustrySerializer(industries, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        if 'file' in request.FILES:
          csv_file = request.FILES['file']
          decoded_file = csv_file.read().decode('utf-8').splitlines()
          reader = csv.DictReader(decoded_file)
     
          for row in reader:
             serializer = IndustrySerializer(data=row)
             if serializer.is_valid():
                serializer.save()

          return Response('Industries added successfully from CSV', status=status.HTTP_201_CREATED)

        else:
           serializer = IndustrySerializer(data=request.data)
           if serializer.is_valid():
              serializer.save()
              return Response('Industry added successfully', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            industry = Industry.objects.get(pk=pk)
        except Industry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = IndustrySerializer(industry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Industry updated successfully')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            industry = Industry.objects.get(pk=pk)
        except Industry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        industry.delete()
        return Response('Industry deleted successfully',status=status.HTTP_204_NO_CONTENT)
    



@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def department(request, pk=None):
    if request.method == 'GET':
        if pk is not None:
            try:
                department = Department.objects.get(pk=pk)
                serializer = DepartmentSerializer(department)
                return Response(serializer.data)
            except Department.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        if 'file' in request.FILES:
          csv_file = request.FILES['file']
          decoded_file = csv_file.read().decode('utf-8').splitlines()
    
            # Process the CSV file
          for line in decoded_file[1:]: 
                fields = line.split(",")
                if len(fields) > 1:  
                    try:
                        industry_ids = fields[2].split(',')
                        
                        
                        department_data = {
                        'department_name': fields[1],
                        'industry':industry_ids
                        }
                    
                        serializer = DepartmentSerializer(data=department_data)
                        if serializer.is_valid():
                          department = serializer.save()
                          print(f"department saved: {department}")
                        else:
                         print(f"Validation errors: {serializer.errors}")
                        
                    except Exception as e:
                         print(f"Error processing line {line}: {e}")
            
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
          serializer = DepartmentSerializer(data=request.data)        
          if serializer.is_valid():
            serializer.save()
            return Response('Department added successfully', status=status.HTTP_201_CREATED)
        
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

          
    elif request.method == 'PATCH':
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
    
        department_data = request.data  
        industry_ids = department_data.get('industry')            
        department_serializer = DepartmentSerializer(department, data=department_data, partial=True)

        if department_serializer.is_valid():
            department_instance = department_serializer.save()  
        
            if industry_ids is not None:  
                department_instance.industry.set(industry_ids)  
        
                return Response(department_serializer.data, status=status.HTTP_200_OK)
        # else:
        return Response(department_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    elif request.method == 'DELETE':
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response({ 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
        department.delete()
        return Response('Department deleted successfully',status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def skills(request, pk=None):
    if request.method == 'GET':
        if pk is not None:
            try:
                skill = Skill.objects.get(pk=pk)
                serializer = SkillSerializer(skill)
                return Response(serializer.data)
            except Skill.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            skills = Skill.objects.all()
            serializer = SkillSerializer(skills, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                serializer = SkillSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
            return Response('Skills added successfully from CSV', status=status.HTTP_201_CREATED)
        
        else:
          serializer = SkillSerializer(data=request.data)
          if serializer.is_valid():
            serializer.save()
            return Response('Skill added successfully', status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            skill = Skill.objects.get(pk=pk)
        except Skill.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SkillSerializer(skill, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Skill updated successfully')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            skill = Skill.objects.get(pk=pk)
        except Skill.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        skill.delete()
        return Response('Skill deleted successfully',status=status.HTTP_204_NO_CONTENT)




@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def company(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                company = Company.objects.prefetch_related('locations').get(pk=pk)
                serializer = CompanySerializer3(company)
                return Response(serializer.data)
            except Company.DoesNotExist:
                return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            companies = Company.objects.prefetch_related('locations').all()
            serializer = CompanySerializer3(companies, many=True)
            return Response(serializer.data)

    

    elif request.method == 'POST':
        if 'file' in request.FILES:
          csv_file = request.FILES['file']
          decoded_file = csv_file.read().decode('utf-8').splitlines()
    
            # Process the CSV file
          for line in decoded_file[1:]: 
                fields = line.split(",")
                if len(fields) > 1:  
                    try:
                        industry_ids = fields[5].split(',')
                        
                        
                        company_data = {
                        'company_name': fields[1],
                        'phone_number': fields[2],
                        'email': fields[3],
                        'website': fields[4],
                        'founded_date': fields[6],
                        'company_size': fields[7],
                        'description': fields[9],
                        'industry':industry_ids
                        }
                    
                        serializer = CompanySerializer(data=company_data)
                        if serializer.is_valid():
                          company = serializer.save()
                          print(f"Company saved: {company}")
                        else:
                         print(f"Validation errors: {serializer.errors}")
                        
                    except Exception as e:
                         print(f"Error processing line {line}: {e}")
            
          return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
          validate_data = request.data
          serializer = CompanySerializer3(data=validate_data)
          if serializer.is_valid():
            serializer.save()
            return Response({"message": "Company Added Successfully", "success": True})
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            company = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
    
        company_data = request.data  
        industry_ids = company_data.get('industry')
    
        company_serializer = CompanySerializer3(company, data=company_data, partial=True)
        if company_serializer.is_valid():
            company_instance = company_serializer.save()
        
            if industry_ids is not None:
                company_instance.industry.set(industry_ids)
        
            return Response(company_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            company = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        company.delete()
        return Response('Company deleted successfully', status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def location(request, company_id=None, location_id=None):
    if request.method == 'GET':
        if company_id:
            try:
                locations = Location.objects.filter(company_id=company_id)
                serializer = LocationSerializer(locations, many=True)
                return Response(serializer.data)
            except Company.DoesNotExist:
                return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        elif location_id:
            try:
                location = Location.objects.get(pk=location_id)
                serializer = LocationSerializer(location)
                return Response(serializer.data)
            except Location.DoesNotExist:
                return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            locations = Location.objects.all()
            serializer = LocationSerializer(locations, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        if 'file' in request.FILES:
          csv_file = request.FILES['file']
          decoded_file = csv_file.read().decode('utf-8').splitlines()
          reader = csv.DictReader(decoded_file)
     
          for row in reader:
             serializer = LocationSerializer(data=row)
             if serializer.is_valid():
                serializer.save()
          return Response(serializer.data)

        #   return Response('Companies added successfully from CSV', status=status.HTTP_201_CREATED)

        else:
          serializer = LocationSerializer(data=request.data)
          if serializer.is_valid():
            serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == 'PATCH':
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({'Location not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({ 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
        location.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)


# @permission_classes([IsAuthenticated])
class FilterDepartment(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DepartmentFilter


# @permission_classes([IsAuthenticated])
class FilterCompany(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class =CompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyFilter
