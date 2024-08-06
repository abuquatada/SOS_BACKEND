from django.shortcuts import render
from rest_framework.response import Response
from application.serializers import *
from application.models import *
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
from django.db.models import Count








@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def application(request, pk=None):
    if request.method == 'GET':
        
        if pk:
            try:
                application = Application.objects.filter(application_id=pk)
                serializer = ApplicationSerializer(application,many=True)
                return Response(serializer.data)
            except Application.DoesNotExist:
                return Response({'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            applications = Application.objects.all()
            serializer = ApplicationSerializer(applications, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        data=request.data
        serializer = ApplicationSerializer(data=data)
        print(request.data)
        if serializer.is_valid():
            
            serializer.save()
            
            return Response('Added Successfully', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Application updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({ 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        application.delete()
        return Response('Application deleted Successfully',status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def applicationstatus(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                application_status = ApplicationStatus.objects.get(pk=pk)
                serializer = ApplicationStatusSerializer(application_status)
                return Response(serializer.data)
            except ApplicationStatus.DoesNotExist:
                return Response({'ApplicationStatus not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            application_statuses = ApplicationStatus.objects.all()
            serializer = ApplicationStatusSerializer(application_statuses, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':


        serializer = ApplicationStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            application_status = ApplicationStatus.objects.get(pk=pk)
        except ApplicationStatus.DoesNotExist:
            return Response({'Application Status not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicationStatusSerializer(application_status, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Application status updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            application_status = ApplicationStatus.objects.get(pk=pk)
        except ApplicationStatus.DoesNotExist:
            return Response({ 'ApplicationStatus not found'}, status=status.HTTP_404_NOT_FOUND)
        application_status.delete()
        return Response('Application status deleted Successfully',status=status.HTTP_204_NO_CONTENT)



@csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
def applicationstatuslog(request, pk=None):
    if request.method == 'GET':
        if pk:
            try:
                application_status_log = ApplicationStatusLog.objects.get(pk=pk)
                serializer = ApplicationStatusLogSerializer(application_status_log)
                return Response(serializer.data)
            except ApplicationStatusLog.DoesNotExist:
                return Response({'ApplicationStatusLog not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            application_status_logs = ApplicationStatusLog.objects.all()
            serializer = ApplicationStatusLogSerializer(application_status_logs, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
       
        serializer = ApplicationStatusLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Added Successfully', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        try:
            application_status_log = ApplicationStatusLog.objects.get(pk=pk)
        except ApplicationStatusLog.DoesNotExist:
            return Response({'ApplicationStatusLog not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicationStatusLogSerializer(application_status_log, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Updated Successfully',)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            application_status_log = ApplicationStatusLog.objects.get(pk=pk)
        except ApplicationStatusLog.DoesNotExist:
            return Response({ 'ApplicationStatusLog not found'}, status=status.HTTP_404_NOT_FOUND)
        application_status_log.delete()
        return Response('Deleted Successfully',status=status.HTTP_204_NO_CONTENT)
    


# @permission_classes([IsAuthenticated])
class FilterApplicationStatusLog(generics.ListAPIView):
    queryset = ApplicationStatusLog.objects.all()
    serializer_class = ApplicationStatusLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicationStatusLogFilter

# @permission_classes([IsAuthenticated])
class FilterApplication(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicationFilter

