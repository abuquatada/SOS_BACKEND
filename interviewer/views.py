from django.shortcuts import render
from rest_framework.response import Response
from .serializer import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status,generics
from rest_framework.filters import SearchFilter 
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *


@api_view(['GET','POST','PATCH','DELETE'])
def InterviewerViews(request, pk=None):
    
    if request.method=='GET':
        if pk is not None:
            try:
                Interviewerobj=Interviewer.objects.get(pk=pk)
                serializers=InterviewerSerializer(Interviewerobj)
                return Response(serializers.data)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            Interviewerobj=Interviewer.objects.all()
            serializers=InterviewerSerializer(Interviewerobj,many=True).data
            return Response(serializers)
        
    elif request.method=='POST':
        try:
          interviewer_data=request.data
        except:
            return Response (status=status.HTTP_404_NOT_FOUND)
        serializers=InterviewerSerializer(data=interviewer_data)
        if serializers.is_valid():
            serializers.save()
            return Response('Interviewer Added ',status=status.HTTP_200_OK)
        
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)
    elif request.method=='PATCH':
        try:
            interviewer_data=Interviewer.objects.get(pk=pk)
            print(interviewer_data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers=InterviewerSerializer(interviewer_data,data=request.data,partial=True)
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
                serializers=InterviewSerializer(interview_obj)
                return Response(serializers.data)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            interview_obj=Interview.objects.all()
            serializers=InterviewSerializer(interview_obj,many=True)
            # print(serializers.data)
            return Response(serializers.data)
        
    elif request.method=='POST':
        try:
         interview_obj=request.data
         print('\n\n\n',interview_obj,'\n\n\n')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers=InterviewSerializer(data=interview_obj)
        if serializers.is_valid():
            serializers.save()
            return Response('Interview Added',status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)
    
    elif request.method=='PATCH':
        try:
          interview_obj=Interview.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers= InterviewSerializer(interview_obj,data=request.data,partial=True)
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
    
class FilterInterviewer(generics.ListAPIView):
    queryset=Interviewer.objects.all()
    serializer_class=InterviewerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class=InterviewerFilter

class FilterInterview(generics.ListAPIView):
    queryset=Interview.objects.all()
    serializer_class=InterviewSerializer
    filter_backends=[SearchFilter]
    search_fields=['status']
    
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def InterviewPhaseView(request, pk=None):
    if request.method == 'GET':
        if pk is not None:
            try:
                phase_obj = InterviewPhase.objects.get(pk=pk)
                serializers = InterviewPhaseSerializer(phase_obj)
                return Response(serializers.data)
            except InterviewPhase.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            phase_objs = InterviewPhase.objects.all()
            serializers = InterviewPhaseSerializer(phase_objs, many=True)
            return Response(serializers.data)
        
    elif request.method == 'POST':
        serializers = InterviewPhaseSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response('Interview Phase Added', status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        try:
            phase_obj = InterviewPhase.objects.get(pk=pk)
        except InterviewPhase.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers = InterviewPhaseSerializer(phase_obj, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response('Interview Phase Updated Successfully', status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            phase_obj = InterviewPhase.objects.get(pk=pk)
        except InterviewPhase.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        phase_obj.delete()
        return Response('Interview Phase Deleted Successfully', status=status.HTTP_200_OK)
    
    
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def InterviewQuestionView(request, pk=None):
    if request.method == 'GET':
        if pk is not None:
            try:
                question_obj = InterviewQuestion.objects.get(pk=pk)
                serializers = InterviewQuestionSerializer(question_obj)
                return Response(serializers.data)
            except InterviewQuestion.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            question_objs = InterviewQuestion.objects.all()
            serializers = InterviewQuestionSerializer(question_objs, many=True)
            return Response(serializers.data)
        
    elif request.method == 'POST':
        serializers = InterviewQuestionSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response('Interview Question Added', status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        try:
            question_obj = InterviewQuestion.objects.get(pk=pk)
        except InterviewQuestion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers = InterviewQuestionSerializer(question_obj, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response('Interview Question Updated Successfully', status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            question_obj = InterviewQuestion.objects.get(pk=pk)
        except InterviewQuestion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        question_obj.delete()
        return Response('Interview Question Deleted Successfully', status=status.HTTP_200_OK)
    
class FilterInterviewQuestion(generics.ListAPIView):
    queryset=InterviewQuestion.objects.all()
    serializer_class=InterviewQuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InterviewQuestionFilter


