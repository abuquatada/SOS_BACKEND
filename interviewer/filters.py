import django_filters
from .models import *


class InterviewQuestionFilter(django_filters.FilterSet):
    phase = django_filters.CharFilter(field_name='phase__phase_name' , lookup_expr='icontains',label='Phase')
    questions_text = django_filters.CharFilter(field_name='question_text', lookup_expr='icontains',label='questions_text')

    class Meta:
        model = InterviewQuestion
        fields = ['phase','questions_text']

class InterviewerFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name',lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name',lookup_expr='icontains')
    gender = django_filters.CharFilter(field_name='gender',lookup_expr='icontains')
    date_of_birth = django_filters.CharFilter(field_name='date_of_birth',lookup_expr='icontains')
    phone_number = django_filters.CharFilter(field_name='phone_number',lookup_expr='icontains')
    language = django_filters.CharFilter(field_name='language',lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email',lookup_expr='icontains')
    total_years_of_experience = django_filters.NumberFilter(field_name='total_years_of_experience',lookup_expr='icontains')
    gender = django_filters.CharFilter(field_name='gender',lookup_expr='icontains')

    class Meta:
        model = Interviewer
        fields = ['first_name', 'last_name','email', 'total_years_of_experience', 'gender','date_of_birth','phone_number','language']
        
        
class InterviewFilter(django_filters.FilterSet):
    application_id = django_filters.NumberFilter(field_name='application_id',lookup_expr='icontains')
    phase_name = django_filters.CharFilter(field_name='phase__phase_name',lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type',lookup_expr='icontains')
    scheduled_date = django_filters.DateFilter(field_name='scheduled_date',lookup_expr='icontains')
    interviewer_id = django_filters.NumberFilter(field_name='interviewer_id',lookup_expr='icontains')
    interviewer_first_name = django_filters.CharFilter(field_name='interviewer__first_name',lookup_expr='icontains')
    interviewer_last_name = django_filters.CharFilter(field_name='interviewer__last_name',lookup_expr='icontains')
    location = django_filters.CharFilter(field_name='location',lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status',lookup_expr='icontains')

    class Meta:
        model = Interview
        fields = ['application_id', 'phase_name', 'type', 'scheduled_date','interviewer_id','location','status','interviewer_first_name','interviewer_last_name']

