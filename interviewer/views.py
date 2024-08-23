from django.shortcuts import render
from rest_framework.response import Response
from .serializer import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status,generics
from rest_framework.filters import SearchFilter 
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404



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


SERVICE_ACCOUNT_FILE = 'E:\Git_sos\SOS_BACKEND\project\sos.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)

def create_event(interview):
    try:
        service = get_google_calendar_service()

        scheduled_datetime = datetime.strptime(interview.scheduled_date, '%Y-%m-%d')

        event = {
            'summary': f'Interview with {interview.application_id}',
            'description': 'Virtual interview via Google Meet',
            'start': {
                'dateTime': scheduled_datetime.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': (scheduled_datetime + timedelta(hours=1)).isoformat(),
                'timeZone': 'UTC',
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': f"{interview.interview_id}-{int(scheduled_datetime.timestamp())}",
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    },
                },
            }
        }

        event_result = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()

        return event_result['hangoutLink']

    except Exception as e:
        print(f"An error occurred while creating the Google Meet event: {e}")
        return None

class ScheduleInterviewView(APIView):
    def post(self, request, applicant_id):
        application = get_object_or_404(Application, applicant_id=applicant_id)
        
        
        interview_data = {
            'application_id': application,
            'phase': request.data.get('phase'),
            'type': request.data.get('type', 'Onsite'),
            'scheduled_date': request.data.get('scheduled_date'),
            'interviewer': get_object_or_404(Interviewer, Interviewer_id=request.data.get('interviewer')),
            'location': request.data.get('location', ''),
            'status': request.data.get('status', 'Scheduled'),
            'notes': request.data.get('notes', '')
        }
        
     
        interview = Interview(**interview_data)

        if interview.type == 'Virtual':
            interview.virtual_link = create_event(interview)
        
        interview.save()
        
        return Response({
            'message': 'Interview scheduled successfully',
            'interview_id': interview.interview_id,
            'virtual_link': interview.virtual_link
        }, status=status.HTTP_201_CREATED)