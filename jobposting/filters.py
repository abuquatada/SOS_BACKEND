import django_filters
from .models import *

class JobPostingFilter(django_filters.FilterSet):
    department_id = django_filters.NumberFilter(field_name='department_id')
    industry_id = django_filters.NumberFilter(field_name='industry_id')
    company = django_filters.NumberFilter(field_name='company')
    job_title = django_filters.CharFilter(field_name='job_title')
    job_position = django_filters.CharFilter(field_name='job_position')
    job_type = django_filters.CharFilter(field_name='job_type')
    skills = django_filters.NumberFilter(field_name='skills')
    salary = django_filters.RangeFilter(field_name='salary')
    location_type = django_filters.CharFilter(field_name='location_type')
    created_by = django_filters.NumberFilter(field_name='created_by')
    location = django_filters.NumberFilter(field_name='location')

    class Meta:
        model = JobPosting
        fields = ['location', 'created_by','company','location_type','salary','skills','job_type','job_position','job_title','industry_id','department_id']

class JobStatusLogFilter(django_filters.FilterSet):
    job_id = django_filters.NumberFilter(field_name='job_id')
    status_id = django_filters.NumberFilter(field_name='status_id')

    class Meta:
        model = JobStatusLog
        fields = ['job_id', 'status_id']


class DepartmentFilter(django_filters.FilterSet):
    industry = django_filters.NumberFilter(field_name='industry')

    class Meta:
        model = Department
        fields = ['industry']


class CompanyFilter(django_filters.FilterSet):
    Industry = django_filters.NumberFilter(field_name='Industry')

    class Meta:
        model = Company
        fields = ['industry']