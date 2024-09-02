from django.shortcuts import render
from rest_framework.response import Response
from .serializer import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status,generics
from rest_framework.filters import SearchFilter 
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
import csv
from datetime import datetime
from django.core.mail import send_mail
from django.conf import  settings
from .meet import create_google_meet_event





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
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            try:
                for line in reader:
                    date_of_birth = datetime.strptime(line['date_of_birth'], '%m/%d/%Y') if line.get('date_of_birth') else None

                    interviewer, created = Interviewer.objects.get_or_create(
                        email=line['email'],
                        defaults={
                            'first_name': line['first_name'],
                            'last_name': line['last_name'],
                            'gender': line['gender'],
                            'date_of_birth': date_of_birth,
                            'phone_number': line['phone_number'],
                            'total_years_of_experience': line['total_years_of_experience'],
                            'language': line['language'],
                            'about': line['about'],
                        }
                    )

                    if created:
                        interviewer.save()

            except Exception as e:
                return Response(f"Error processing CSV: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response('Interviewers added successfully', status=status.HTTP_201_CREATED)   
        else:
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
        app_id = request.GET.get('app_id')
        if app_id :
            try:
                interview_obj=Interview.objects.filter(application_id=app_id)
                serializers=InterviewSerializer(interview_obj,many=True)
                return Response(serializers.data)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        elif pk is not None:
            try:
                interview_obj=Interview.objects.get(pk=pk)
                serializers=InterviewSerializer(interview_obj)
                return Response(serializers.data)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            interview_obj=Interview.objects.all()
            serializers=InterviewSerializer(interview_obj,many=True)
            return Response(serializers.data)
        
    elif request.method=='POST':
        try:
         interview_obj=request.data
         print('\n\n\n',interview_obj,'\n\n\n')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        application_obj = Application.objects.get(application_id=interview_obj['application_id'])
        interviewer_obj = Interviewer.objects.get(interviewer_id=interview_obj['interviewer'])
        phase_obj = InterviewPhase.objects.get(phase_id=interview_obj['phase'])
        google_meet_link=create_google_meet_event()
        
        scheduled_date = datetime.strptime(interview_obj['scheduled_date'], "%Y-%m-%d %I:%M %p")
        # iso_scheduled_date = scheduled_date.isoformat() + 'Z'
        print('\n\n\n',scheduled_date,'\n\n\n')
        # print('\n\n\n',iso_scheduled_date,'\n\n\n')
        iso_scheduled_date = scheduled_date.isoformat() + 'Z'

        # Update the interview_obj with ISO formatted date
        interview_obj['scheduled_date'] = iso_scheduled_date
        serializers=InterviewSerializer(data=interview_obj)
        if serializers.is_valid():
            if interview_obj['type'] == 'Virtual':
                obj_interview = Interview.objects.create(
                                                        type=interview_obj["type"],
                                                        scheduled_date=scheduled_date, 
                                                        virtual_link=google_meet_link,
                                                        notes=interview_obj["notes"],
                                                        application_id=application_obj,
                                                         phase=phase_obj,
                                                         interviewer=interviewer_obj,
                                                         )
            else:    
                obj_interview = Interview.objects.create(
                                                        type=interview_obj["type"],
                                                        scheduled_date=scheduled_date, 
                                                        location=interview_obj["location"],
                                                        notes=interview_obj["notes"],
                                                         application_id=application_obj,
                                                          phase=phase_obj,
                                                          interviewer=interviewer_obj,
                                                         )
            
            obj_interview.save()
            applicant_user = Application.objects.get(application_id=interview_obj['application_id'])
            applicant_email = applicant_user.applicant_id.id.email
            applicant_name = applicant_user.applicant_id.id.first_name
            
            interviewer_id= interview_obj['interviewer']
            interviewer_instance = Interviewer.objects.get(interviewer_id=interviewer_id)
            interviewer_firstname=interviewer_instance.first_name
            interviewer_email=interviewer_instance.email

            application_id = interview_obj['application_id']
            companies_instance=Application.objects.get(application_id=application_id)
            company_name=companies_instance.company_id.company_name


            subject_applicant = f'Interview Invitation at {company_name}'
            message_applicant = (
            f'Dear {applicant_name},\n\n'
            f'Thank you for applying at {company_name}. We have reviewed your application and are pleased to invite you to an interview to further discuss your qualifications and the role.\n\n'
            'Best regards,\n'
            )
            send_mail(subject_applicant, message_applicant, settings.EMAIL_HOST_USER, [applicant_email])

            subject_interviewer = 'You have been scheduled to conduct an interview'
            message_interviewer = (
            f'Dear {interviewer_firstname},\n\n'
            f'Please review the candidate\'s  resume and prepare any questions you may have. If the interview is virtual, the meeting link is attached below.\n\n'
            'Best regards,\n'

            )
            send_mail(subject_interviewer, message_interviewer, settings.EMAIL_HOST_USER, [interviewer_email])
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
    filter_backends=[DjangoFilterBackend]
    filterset_class=InterviewFilter
    
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


@api_view(["GET", "PUT", "POST", "DELETE"])
def Interview_Feedback_View(request, pk=None):
    if request.method == "GET":
        if pk is not None:
            try:
                feedback_obj = Interview_feedback.objects.get(feedback_id=pk)
                serializer = Interview_feedback_Serializer(feedback_obj, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(
                    data={"message": "Data not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            feedback_obj = Interview_feedback.objects.all()
            serializer = Interview_feedback_Serializer(feedback_obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        data = request.data
        serializer = Interview_feedback_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Data Saved Successfully!"}, status=status.HTTP_201_CREATED
            )
        return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == "PUT":
        try:
            if pk is not None:
                obj = Interview_feedback.objects.get(feedback_id=pk)
                serializer = Interview_feedback_Serializer(
                    data=request.data, instance=obj
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"message": "data updated successfully!"},
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        try:
            objToDelete = Interview_feedback.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        objToDelete.delete()
        return Response(
            {"message": "Row Deleted Successfully!"}, status=status.HTTP_200_OK
        )
        
        
@api_view(['POST'])
def InterviewerCSV(request, format=None):

    csv_file = request.FILES['file']
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)

    try:
        for line in reader:
            date_of_birth = datetime.strptime(line['date_of_birth'], '%m/%d/%Y') if line.get('date_of_birth') else None

            interviewer, created = Interviewer.objects.get_or_create(
                email=line['email'],
                defaults={
                    'first_name': line['first_name'],
                    'last_name': line['last_name'],
                    'gender': line['gender'],
                    'date_of_birth': date_of_birth,
                    'phone_number': line['phone_number'],
                    'total_years_of_experience': line['total_years_of_experience'],
                    'language': line['language'],
                    'about': line['about'],
                }
            )

            if created:
                interviewer.save()

    except Exception as e:
        return Response(f"Error processing CSV: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response('Interviewers added successfully', status=status.HTTP_201_CREATED)        





#-----------GOOGLE MEET CODE--------------------
# from rest_framework import exceptions
# import logging
# import uuid
# from django.core.mail import send_mail
# from django.conf import  settings
# import csv
# from datetime import datetime
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# import os
# from django.http import HttpResponseRedirect
# from rest_framework.views import APIView

# OAUTHLIB_INSECURE_TRANSPORT= 1

# CLIENT_CONFIG = {
#     "web": {
#     "client_id": "630519295088-juf629tr6av6brod4hmuaj9mb6u19jqr.apps.googleusercontent.com",
#         "redirect_uris": ["http://127.0.0.1:8000/google/calendar/redirect/"],
#     "project_id": "switchonsuccess",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_secret": "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"
#   }
# }
# SCOPES = [
#     'https://www.googleapis.com/auth/calendar.events',
#     'https://www.googleapis.com/auth/calendar'
# ]

# logger = logging.getLogger(__name__)

# class GoogleCalendarInitView(APIView):
#     def get(self, request):
#         try:
#             interview_id = request.query_params.get('interview_id')
#             date_str = request.query_params.get('scheduled_date')

#             if not interview_id or not date_str:
#                 return Response({"error": "Missing interview_id or scheduled_date"}, status=status.HTTP_400_BAD_REQUEST)

#             try:
#                 scheduled_date = datetime.strptime(date_str, '%Y-%m-%d').date()
#             except ValueError:
#                 return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

#             state = str(uuid.uuid4())
#             request.session['state'] = state
#             request.session['interview_id'] = interview_id
#             request.session['scheduled_date'] = scheduled_date.isoformat()

#             flow = Flow.from_client_config(CLIENT_CONFIG, SCOPES)
#             flow.redirect_uri = "http://127.0.0.1:8000/google/calendar/redirect/"
#             authorization_url, _ = flow.authorization_url(state=state)

#             return HttpResponseRedirect(authorization_url)
#         except Exception as e:
#             logger.error(f'Error in GoogleCalendarInitView: {str(e)}')
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class GoogleCalendarRedirectView(APIView):
#     def set_session(self, request, credentials):
#         request.session['credentials'] = {
#             'token': credentials.token,
#             'refresh_token': credentials.refresh_token,
#             'token_uri': credentials.token_uri,
#             'client_id': credentials.client_id,
#             'client_secret': credentials.client_secret,
#             'scopes': credentials.scopes,
#         }

#     def process_events(self, credentials, interview_id, scheduled_date):
#         try:
#             service = build('calendar', 'v3', credentials=credentials)

#             event = {
#                 'summary': 'Google Meet with Team',
#                 'description': 'A Google Meet to discuss project details.',
#                 'start': {
#                     'dateTime': f'{scheduled_date}T10:00:00-07:00',
#                     'timeZone': 'America/Los_Angeles',
#                 },
#                 'end': {
#                     'dateTime': f'{scheduled_date}T11:00:00-07:00',
#                     'timeZone': 'America/Los_Angeles',
#                 },
#                 'conferenceData': {
#                     'createRequest': {
#                         'requestId': str(uuid.uuid4()),
#                         'conferenceSolutionKey': {'type': 'hangoutsMeet'}
#                     }
#                 },
#                 'attendees': [{'email': 'example@example.com'}],
#                 'reminders': {
#                     'useDefault': False,
#                     'overrides': [{'method': 'email', 'minutes': 24 * 60}, {'method': 'popup', 'minutes': 10}],
#                 },
#             }

#             created_event = service.events().insert(
#                 calendarId='primary',
#                 body=event,
#                 conferenceDataVersion=1
#             ).execute()

#             meet_link = created_event.get('hangoutLink', 'No Meet Link')

#             from .models import Interview
#             try:
#                 interview = Interview.objects.get(interview_id=interview_id)
#                 interview.virtual_link = meet_link
#                 interview.save()
#             except Interview.DoesNotExist:
#                 return Response({"error": "Interview not found"}, status=status.HTTP_404_NOT_FOUND)

#             return Response({'message': 'Event created', 'meet_link': meet_link, "scheduled_date": scheduled_date})
#         except Exception as e:
#             logger.error(f'Error in process_events: {str(e)}')
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def get(self, request):
#         try:
#             state = request.session.get('state')
#             interview_id = request.session.get('interview_id')
#             scheduled_date = request.session.get('scheduled_date')

#             if not state or not interview_id or not scheduled_date:
#                 return Response({"error": "Missing state, interview_id, or scheduled_date"}, status=status.HTTP_400_BAD_REQUEST)

#             flow = Flow.from_client_config(CLIENT_CONFIG, SCOPES)
#             flow.redirect_uri = "http://127.0.0.1:8000/google/calendar/redirect/"
#             flow.fetch_token(authorization_response=request.build_absolute_uri())

#             credentials = flow.credentials
#             self.set_session(request, credentials)

#             return self.process_events(credentials, interview_id, scheduled_date)
#         except Exception as e:
#             logger.error(f'Error in GoogleCalendarRedirectView: {str(e)}')
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)