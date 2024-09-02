from django.shortcuts import render
from rest_framework.response import Response
from .serializer import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status,generics
from rest_framework.filters import SearchFilter 
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.conf import settings
from google.oauth2.credentials import Credentials
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
import os
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import argparse
from oauth2client import tools
from django.shortcuts import get_object_or_404
import json
from googleapiclient.errors import HttpError






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

def google_authenticate(request):
    print("google_authenticate view called") 
    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'sos.json'),
        scopes=['https://www.googleapis.com/auth/calendar.events',
                'https://www.googleapis.com/auth/forms.body','https://www.googleapis.com/auth/forms.responses.readonly'],
        redirect_uri='http://localhost:8080/'
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    print(f"Authorization URL: {authorization_url}")

    request.session['state'] = state
    print(f"Generated state: {state}")
    print(f"Session state set: {request.session.get('state')}")
    
    return redirect(authorization_url)

def google_authenticate(request):
    print("google_authenticate view called") 
    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'sos.json'),
        scopes=['https://www.googleapis.com/auth/calendar.events',
                'https://www.googleapis.com/auth/forms.body','https://www.googleapis.com/auth/forms.responses.readonly'],
        redirect_uri='http://127.0.0.1:8000/google/callback/'
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    print(f"Authorization URL: {authorization_url}")


    request.session['state'] = state
    print(f"Generated state: {state}")
    print(f"Session state set: {request.session.get('state')}")
    
    return redirect(authorization_url)

def google_callback_view(request):
    stored_state = request.session.get('state')
    returned_state = request.GET.get('state')
    print(f"Stored state: {stored_state}")
    print(f"Returned state: {returned_state}")

    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'sos.json'),
        scopes=['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/forms.responses.readonly'],
        state=returned_state,
        redirect_uri='http://localhost:8080/'
    )
    authorization_response = request.build_absolute_uri()
    
    try:
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        credentials_data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        credentials_file = os.path.join(settings.BASE_DIR, 'credentials.json')
        with open(credentials_file, 'w') as f:
            json.dump(credentials_data, f)
        print(f"Stored credentials in file: {credentials_file}")
        return redirect('create_and_schedule_interview')
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def create_google_meet_link(request, interview):
    credentials_file = os.path.join(settings.BASE_DIR, 'credentials.json')
    
    if not os.path.exists(credentials_file):
        print("Credentials file not found. Redirecting to Google authentication.")
        return redirect('google_authenticate')

    with open(credentials_file, 'r') as f:
        credentials_data = json.load(f)

    creds = Credentials(**credentials_data)
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': f'Interview: {interview.phase}',
        'description': interview.notes,
        'start': {
            'dateTime': interview.scheduled_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (interview.scheduled_date + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'UTC',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': f"{interview.application_id}",
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
                'status': {
                    'statusCode': 'success'
                }
            },
        },
    }
    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    return event['hangoutLink']

@api_view(['POST'])
def create_and_schedule_interview(request):
    try:
        application_id = request.data.get('application_id')
        phase = request.data.get('phase')
        interview_type = request.data.get('type', 'Onsite')
        scheduled_date_str = request.data.get('scheduled_date')
        interviewer_id = request.data.get('interviewer')
        location = request.data.get('location')
        status_field = request.data.get('status')
        notes = request.data.get('notes')

        if not all([application_id, phase, scheduled_date_str, interviewer_id, status_field]):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        scheduled_date = datetime.strptime(scheduled_date_str, '%Y-%m-%dT%H:%M:%S')

        application = Application.objects.get(pk=application_id)
        interviewer = Interviewer.objects.get(pk=interviewer_id)

        interview = Interview.objects.create(
            application_id=application,
            phase=phase,
            type=interview_type,
            scheduled_date=scheduled_date,
            interviewer=interviewer,
            location=location,
            status=status_field,
            notes=notes
        )
        request.session['interview_id'] = interview.interview_id

        if interview_type == 'Virtual':
            meet_link = create_google_meet_link(request, interview)
            if isinstance(meet_link, HttpResponseRedirect):
                return meet_link  
            interview.virtual_link = meet_link
        
        interview.save()

        form_url = create_google_form()
        applicant_email = application.applicant_id.id.email
        send_form_email(applicant_email, form_url)

        return JsonResponse({
            'status': 'success',
            'interview_id': interview.interview_id,
            'virtual_link': interview.virtual_link if interview.type == 'Virtual' else None,
            'form_url': form_url
        }, status=status.HTTP_201_CREATED)

    except Application.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
    except Interviewer.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Interviewer not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
SCOPES = ['https://www.googleapis.com/auth/calendar.events',
            'https://www.googleapis.com/auth/forms.body','https://www.googleapis.com/auth/forms.responses.readonly']
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

TOKEN_FILE = 'token.json' 
  
def create_google_form():
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    flags = parser.parse_args([]) 

    store = file.Storage(TOKEN_FILE)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(settings.GOOGLE_CLIENT_SECRETS_FILE, SCOPES , redirect_uri='http://localhost:8080/')
        creds = tools.run_flow(flow, store, flags) 

    form_service = discovery.build(
        "forms", "v1", http=creds.authorize(Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False
    )
    NEW_FORM = {
        "info": {
            "title": "Interview Feedback Form",
        }
    }

    NEW_QUESTION = {
        "requests": [
            {
                "createItem": {
                    "item": {
                        "title": "How satisfied were you with the interview process?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": "Very Satisfied"},
                                        {"value": "Satisfied"},
                                        {"value": "Neutral"},
                                        {"value": "Dissatisfied"},
                                        {"value": "Very Dissatisfied"},
                                    ],
                                    "shuffle": True,
                                },
                            }
                        },
                    },
                    "location": {"index": 0},
                }
            }
        ]
    }

    result = form_service.forms().create(body=NEW_FORM).execute()
    form_id = result["formId"]
    form_service.forms().batchUpdate(formId=form_id, body=NEW_QUESTION).execute()

    form_url = f"https://docs.google.com/forms/d/{form_id}/viewform"
    return  form_url , form_id

def send_form_email(applicant_email, form_url):
    subject = "Your Interview Feedback Form"
    message = f"Dear Applicant,\n\nPlease fill out the interview feedback form using the following link:\n{form_url}\n\nBest regards,\nYour Company"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [applicant_email]
    send_mail(subject, message, email_from, recipient_list)
    
def form_responses(request, form_id):

    credentials_file = os.path.join(settings.BASE_DIR, 'credentials.json')
    
    if not os.path.exists(credentials_file):
        return JsonResponse({'error': 'Credentials file not found. Please authenticate first.'}, status=400)
    
    with open(credentials_file, 'r') as f:
        credentials_data = json.load(f)

    creds = Credentials(**credentials_data)
    
    try:
        service = build('forms', 'v1', credentials=creds)

        response = service.forms().responses().list(formId=form_id).execute()

        return JsonResponse(response)
    
    except HttpError as error:

        return JsonResponse({'error': f'An error occurred: {error}'}, status=400)