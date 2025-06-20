from django.urls import path,include
from app.views import *
from applicant.views import *
from recruiter.views import *
from application.views import *
from jobposting.views import *
from interviewer.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('users/',User.as_view()),
    path('login/', login_view),
    path('logout/',Logout.as_view()),
    path('passwordreset_request/',PasswordResetRequestView.as_view()),
    path('passwordresetconfirm/<str:id>/<str:token>/', PasswordResetConfirmView.as_view()),
    path('change_password/', ChangePassword.as_view()),
    path('complete_profile_applicant/',complete_profile_applicant),
    path('complete_profile_recruiter/',complete_profile_recruiter),
    path('industry/', industry),
    path('industry/<int:pk>/', industry),
    path('roles/', roles),
    path('roles/<int:pk>/', roles),
    path('department/', department),
    path('department/<int:pk>/', department),
    path('skills/', skills),
    path('skills/<int:pk>/', skills),
    path('company/', company),
    path('company/<int:pk>/', company),
    path('location/', location),
    path('location/<int:company_id>/', location),
    path('location/location_id/<int:location_id>/',location),
    path('applicant/', applicant),
    path('applicant/<int:pk>/', applicant),
    path('applicant_education/', applicant_education),
    path('applicant_education/<int:pk>/', applicant_education),
    path('applicant_experience/', applicant_experience),
    path('applicant_experience/<int:pk>/', applicant_experience),
    path('applicant_internship/', applicant_internship),
    path('applicant_internship/<int:pk>/', applicant_internship),
    path('applicant_certification/', applicant_certification),
    path('applicant_certification/<int:pk>/', applicant_certification),        
    path('recruiter/', recruiter),
    path('recruiter/<int:pk>/', recruiter),   
    path('recruiter_education/', recruiter_education),
    path('recruiter_education/<int:pk>/', recruiter_education),
    path('recruiter_experience/', recruiter_experience),
    path('recruiter_experience/<int:pk>/', recruiter_experience),
    path('recruiter_certification/', recruiter_certification),
    path('recruiter_certification/<int:pk>/', recruiter_certification),
    path('jobstatus/', jobstatus),
    path('jobstatus/<int:pk>/', jobstatus),
    path('jobposting/', jobposting),
    path('jobposting/<int:pk>/', jobposting),
    path('jobstatuslog/', jobstatuslog),
    path('jobstatuslog/<int:pk>/', jobstatuslog),
    path('application/', application),
    path('application/<int:pk>/', application),
    path('applicationstatus/', applicationstatus),
    path('applicationstatus/<int:pk>/', applicationstatus),
    path('applicationstatuslog/', applicationstatuslog),
    path('applicationstatuslog/<int:pk>/', applicationstatuslog),
    path('filter-application-status-logs/', FilterApplicationStatusLog.as_view(), name='filter-application-status-logs'),
    path('filter-application/', FilterApplication.as_view(), name='filter-application'),
    path('filter-jobposting/', FilterJobPosting.as_view(), name='filter-jobposting'),
    path('filter-job-status-logs/', FilterJobStatusLog.as_view(), name='filter-job-status-logs'),
    path('filter-department/', FilterDepartment.as_view(), name='filter-department'),
    path('filter-company/', FilterCompany.as_view(), name='filter-company'),
    path('filter-recruiter-education/', FilterRecruiterEducation.as_view(), name='filter-recruiter-education'),
    path('filter-recruiter-experience/', FilterRecruiterExperience.as_view(), name='filter-recruiter-experience'),
    path('filter-recruiter-certification/', FilterRecruiterCertification.as_view(), name='filter-recruiter-certification'),
    path('filter-recruiter/', FilterRecruiter.as_view(), name='filter-recruiter'),
    path('filter-applicant-education/', FilterApplicantEducation.as_view(), name='filter-applicant-education'),
    path('filter-applicant-experience/', FilterApplicantExperience.as_view(), name='filter-applicant-experience'),
    path('filter-applicant-certification/', FilterApplicantCertification.as_view(), name='filter-applicant-certification'),
    path('filter-applicant-internship/', FilterApplicantInternship.as_view(), name='filter-applicant-internship'),
    path('filter-applicants/', FilterApplicant.as_view(), name='filter-applicants'),
    path('send-email-filtered-applicants/', SendEmailToSelectedApplicants),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(serializer_class=CustomTokenRefreshSerializer), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('applicant-details/<int:pk>/', get_applicant_details),
    path('recruiter-details/<int:pk>/', get_recruiter_details),
    ##--------------------------------------------------
    path('get_app/', get_applicant),
    path('get_app/<int:pk>', get_applicant),
    path('get_recruiter/<int:pk>/', get_recruiter),   
    path('application_by_applicant_id/<int:pk>/', get_application),
    path('application_by_applicant_id/recr_id/<int:recr_id>/', get_application),
    path('application_by_job_id/<int:job_id>/', get_application),
    path('recruiter_specific/<int:pk>/', get_recruiter_specific),   
    path('recruiter_specific/', get_recruiter_specific),   
    path('applicant_with_application/', applicant_with_application),  
    path('emp/',emplog),
    path('emp/<int:pk>/',emplog),
    path('filter-emplog/', FilterEmplog.as_view(), name='filter-emplog'),
    path('applicantcount/',applicantcount),
    path('app_status/',application_status_count),
    path('applicationstatuslatestcount/',get_all_application_statuses),
    path('interviewer/',InterviewerViews),
    path('interviewer/<int:pk>/',InterviewerViews),
    path('interview/',InterviewView),
    path('interview/<int:pk>/',InterviewView),
    path('filter-interviewer/',FilterInterviewer.as_view()),
    path('filter-interview/',FilterInterview.as_view()),
    path('interviewphase/',InterviewPhaseView),
    path('interviewphase/<int:pk>/',InterviewPhaseView),
    path('interviewquestions/',InterviewQuestionView),
    path('interviewquestions/<int:pk>/',InterviewQuestionView),
    path('filter-interview-questions/',FilterInterviewQuestion.as_view()),
    path('feedback/', Interview_Feedback_View),
    path('feedback/<int:pk>/', Interview_Feedback_View),
    path('jobpostingcsv/',JobpostingCSV),
    path('applicant-document/',applicant_document),
    path('applicant-document/<int:pk>/',applicant_document),
    path('senduploadlink/<int:job_id>/<int:applicant_id>/', send_document_upload_link),
    path('uploaddocument/<str:token>/', document_upload_view)
]
