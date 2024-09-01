import django_filters
from .models import *


class InterviewQuestionFilter(django_filters.FilterSet):
    phase = django_filters.CharFilter(field_name='phase__phase_name' ,  lookup_expr='icontains')

    class Meta:
        model = InterviewQuestion
        fields = ['phase']

class InterviewerFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name')
    email = django_filters.CharFilter(field_name='email')
    total_years_of_experience = django_filters.NumberFilter(field_name='total_years_of_experience')
    gender = django_filters.CharFilter(field_name='gender')

    class Meta:
        model = Interviewer
        fields = ['first_name', 'email', 'total_years_of_experience', 'gender']

class InterviewFilter(django_filters.FilterSet):
    interview_id = django_filters.NumberFilter()
    application_id = django_filters.NumberFilter(field_name='application_id__application_id')
    phase = django_filters.CharFilter(field_name='phase__phase_name', lookup_expr='icontains')
    type = django_filters.ChoiceFilter(choices=[('Onsite', 'Onsite'), ('Virtual', 'Virtual')])
    scheduled_date = django_filters.DateFilter()
    interviewer = django_filters.CharFilter(field_name='interviewer__first_name', lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    virtual_link = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.CharFilter(lookup_expr='icontains')
    notes = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Interview
        fields = ['interview_id', 'application_id', 'phase', 'type', 'scheduled_date', 
                  'interviewer', 'location', 'virtual_link', 'status', 'notes']
