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
from .meet import *
import logging
import uuid
import os
from google_auth_oauthlib.flow import Flow
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.http import JsonResponse
from googleapiclient.discovery import build





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
            # try:
                interview_obj=Interview.objects.get(pk=pk)
                serializers=InterviewSerializer(interview_obj).data
                if len(serializers['feedback']) == 0:
                    try:
                        form_obj = Google_form.objects.get(interview=serializers['interview_id'])
                        status_id = form_obj.status_question_id
                        rating_id = form_obj.rating_question_id
                        comment_id = form_obj.comments_question_id
                        form_serializer = Google_formSerializer(form_obj).data
                        fetch_response= fetch_and_store_responses(form_serializer['google_form_id'])
                        for key, value in fetch_response['answers'].items():
                            if status_id == value['questionId']:
                                sta = value['textAnswers']['answers'][0]['value']
                                interview_obj_ = Interview.objects.filter(interview_id=interview_obj.interview_id).update(status=sta)
                            if rating_id == value['questionId']:
                                rating_value__ = value['textAnswers']['answers'][0]['value']
                            if comment_id == value['questionId']:
                                comment_value__ = value['textAnswers']['answers'][0]['value']
                        print(f'Rating {rating_value__}')                
                        print(f'Comment {comment_value__}')                
                        inv_feedback_obj = Interview_feedback.objects.create(
                            Interview=interview_obj,
                            rating=rating_value__,
                            comments=comment_value__
                        )  
                        inv_feedback_obj.save()      
                        return Response(serializers)
                    except:
                        return Response(serializers)    
                else:  
                    return Response(serializers)
            # except:
            #     return Response(status=status.HTTP_404_NOT_FOUND)
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
        
        scheduled_date = datetime.strptime(interview_obj['scheduled_date'], "%Y-%m-%d %I:%M %p")
        print('\n\n\n',f'schedule date and time{scheduled_date}','\n\n\n')
        iso_scheduled_date = scheduled_date.isoformat() + 'Z'
        interview_obj['scheduled_date'] = iso_scheduled_date
        
        serializers=InterviewSerializer(data=interview_obj)
        if serializers.is_valid():
            if interview_obj['type'] == 'Virtual':
                google_meet_link=create_google_meet_event()
                obj_interview = Interview.objects.create(
                                                            type=interview_obj["type"],
                                                            scheduled_date=scheduled_date, 
                                                            notes=interview_obj["notes"],
                                                            application_id=application_obj,
                                                            phase=phase_obj,
                                                            interviewer=interviewer_obj,
                                                            virtual_link=google_meet_link
                                                             )
            else:    
                obj_interview = Interview.objects.create(type=interview_obj["type"],
                                                            scheduled_date=scheduled_date, 
                                                            notes=interview_obj["notes"],
                                                            application_id=application_obj,
                                                            phase=phase_obj,
                                                            location=interview_obj['location'],
                                                            interviewer=interviewer_obj,
                                                             )
                
            obj_interview.save()
            
            
            print(f'this is interview{obj_interview.interview_id}','\n\n\n')
            interview_data = {
                "applicant_name":obj_interview.application_id.applicant_id.id.first_name
            }
            question_data=[]
            feedback_form = google_form(interview_data)
            print('\n\n\n',f'feedback data {feedback_form}','\n\n\n')
            for i in feedback_form[1]['replies']:
                d = i['createItem']['questionId']
                question_data.extend(d)
                
            print(question_data)
            feedback_obj = Google_form.objects.create(
                                            google_form_id=feedback_form[0]['formId'],
                                            interview=obj_interview,
                                            feedback_url=feedback_form[0]['responderUri'],
                                            status_question_id=question_data[0],
                                            rating_question_id=question_data[1],
                                            comments_question_id=question_data[2],
                                            )
            feedback_obj.save() 
            
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
            'Best regards,\n\n'
            f'Please provide the interview feedback on this url{subject_applicant}'

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





