import django_filters
from .models import *

class ApplicantEducationFilter(django_filters.FilterSet):
    applicant_id = django_filters.NumberFilter(field_name='applicant_id')
    degree = django_filters.CharFilter(field_name='degree')
    field_of_specialization = django_filters.CharFilter(field_name='field_of_specialization')

    class Meta:
        model = ApplicantEducation
        fields = ['applicant_id','degree','field_of_specialization']



class ApplicantExperiencenFilter(django_filters.FilterSet):
    applicant_id = django_filters.NumberFilter(field_name='applicant_id')

    class Meta:
        model = ApplicantExperience
        fields = ['applicant_id']

class ApplicantCertificationFilter(django_filters.FilterSet):
    applicant_id = django_filters.NumberFilter(field_name='applicant_id')

    class Meta:
        model = ApplicantCertification
        fields = ['applicant_id']


class ApplicantInternshipFilter(django_filters.FilterSet):
    applicant_id = django_filters.NumberFilter(field_name='applicant_id')

    class Meta:
        model = ApplicantInternship
        fields = ['applicant_id']



class ApplicantFilter(django_filters.FilterSet):
    skills = django_filters.NumberFilter(field_name='skills')
    gender = django_filters.CharFilter(field_name='gender')
    martial_status = django_filters.CharFilter(field_name='martial_status')
    home_town = django_filters.CharFilter(field_name='home_town')
    current_location = django_filters.CharFilter(field_name='current_location')
    languages = django_filters.CharFilter(field_name='languages')
    total_years_of_experience = django_filters.NumberFilter(field_name='total_years_of_experience')
    preferred_job_type = django_filters.CharFilter(field_name='preferred_job_type')
    preferred_location = django_filters.CharFilter(field_name='preferred_location')
    interested_industry = django_filters.NumberFilter(field_name='interested_industry')
    interested_department = django_filters.NumberFilter(field_name='interested_department')
    availability_to_join = django_filters.CharFilter(field_name='availability_to_join')
    work_permit_for_USA = django_filters.CharFilter(field_name='work_permit_for_USA')

    class Meta:
        model = Applicants
        fields = ['skills','gender','martial_status','home_town','current_location','languages','total_years_of_experience','preferred_job_type','preferred_location','work_permit_for_USA',
                  'interested_industry','interested_department','availability_to_join']
