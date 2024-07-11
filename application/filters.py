import django_filters
from .models import *

class ApplicationStatusLogFilter(django_filters.FilterSet):
    application_id = django_filters.NumberFilter(field_name='application_id')
    status_id = django_filters.NumberFilter(field_name='status_id')

    class Meta:
        model = ApplicationStatusLog
        fields = ['application_id', 'status_id']


class ApplicationFilter(django_filters.FilterSet):
    applicant_id = django_filters.NumberFilter(field_name='applicant_id')
    job_id = django_filters.NumberFilter(field_name='job_id')
    company_id = django_filters.NumberFilter(field_name='company_id')
    referral_id = django_filters.NumberFilter(field_name='referral_id')

    class Meta:
        model = Application
        fields = ['applicant_id', 'job_id','company_id','referral_id']