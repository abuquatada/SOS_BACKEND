from django.shortcuts import render
from rest_framework.response import Response
from .serializer import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status,generics
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter 


@api_view(['GET','POST','PATCH','DELETE'])
def InterviwerViews(request, pk=None):
    
    if request.method=='GET':
        if pk is not None:
            try:
                Interviewerobj=Interviewer.objects.get(pk=pk)
                serializers=interviwerSerializer(Interviewerobj)
                return Response(serializers.data)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            Interviewerobj=Interviewer.objects.all()
            serializers=interviwerSerializer(Interviewerobj,many=True).data
            return Response(serializers)
        
    elif request.method=='POST':
        try:
          interviewer_data=request.data
        except:
            return Response (status=status.HTTP_404_NOT_FOUND)
        serializers=interviwerSerializer(data=interviewer_data)
        if serializers.is_valid():
            serializers.save()
            return Response('Interviwer Added ',status=status.HTTP_200_OK)
        
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)
    elif request.method=='PATCH':
        try:
            interviewer_data=Interviewer.objects.get(pk=pk)
            print(interviewer_data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers=interviwerSerializer(interviewer_data,data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response('Update Successfully',status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)
    
    elif request.method=='DELETE':
        try:
          interviewer_data=Interviewer.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        interviewer_data.delete()
        return Response('Delete Successfull',status=status.HTTP_200_OK)
    

@api_view(['GET','POST','PATCH','DELETE'])
def InterviewView(request,pk=None):
    if request.method=='GET':
        if pk is not None:
            try:
                interview_obj=Interview.objects.get(pk=pk)
                serializers=interviewSerializer(interview_obj)
                return Response(serializers.data)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            interview_obj=Interview.objects.all()
            serializers=interviewSerializer(interview_obj,many=True)
            # print(serializers.data)
            return Response(serializers.data)
        
    elif request.method=='POST':
        try:
         interview_obj=request.data
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers=interviewSerializer(data=interview_obj)
        if serializers.is_valid():
            serializers.save()
            return Response('Interview Added',status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)
    elif request.method=='PATCH':
        try:
          interview_obj=Interview.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers= interviewSerializer(interview_obj,data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response('Update Seccessfully',status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)
    
    elif request.method=='DELETE':
        try:
            interview_obj=Interview.objects.get(pk=pk)
        except:
            return Response (status=status.HTTP_404_NOT_FOUND)
        interview_obj.delete()
        return Response('Delete Successfully',status=status.HTTP_200_OK)
    
class FilterInterviwer(generics.ListAPIView):
    queryset=Interviewer.objects.all()
    serializer_class=interviwerSerializer
    filter_backends = [SearchFilter]
    search_fields=['first_name']

class FilterInterview(generics.ListAPIView):
    queryset=Interview.objects.all()
    serializer_class=interviewSerializer
    filter_backends=[SearchFilter]
    search_fields=['interview_id']