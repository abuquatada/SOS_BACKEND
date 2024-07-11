import django_filters
from .models import *

class RecruiterEducationFilter(django_filters.FilterSet):
    recruiter_id = django_filters.NumberFilter(field_name='recruiter_id')
    degree = django_filters.CharFilter(field_name='degree')
    field_of_specialization = django_filters.CharFilter(field_name='field_of_specialization')

    class Meta:
        model = RecruiterEducation
        fields = ['recruiter_id','degree','field_of_specialization']



class RecruiterExperiencenFilter(django_filters.FilterSet):
    recruiter_id = django_filters.NumberFilter(field_name='recruiter_id')

    class Meta:
        model = RecruiterExperience
        fields = ['recruiter_id']

class RecruiterCertificationFilter(django_filters.FilterSet):
    recruiter_id = django_filters.NumberFilter(field_name='recruiter_id')

    class Meta:
        model = RecruiterCertification
        fields = ['recruiter_id']




class RecruiterFilter(django_filters.FilterSet):
    companies = django_filters.NumberFilter(field_name='companies')
    gender = django_filters.CharFilter(field_name='gender')
    martial_status = django_filters.CharFilter(field_name='martial_status')
    home_town = django_filters.CharFilter(field_name='home_town')
    current_location = django_filters.CharFilter(field_name='current_location')
    languages = django_filters.CharFilter(field_name='languages')
    total_years_of_experience = django_filters.NumberFilter(field_name='total_years_of_experience')

    class Meta:
        model = Recruiters
        fields = ['companies','gender','martial_status','home_town','current_location','languages','total_years_of_experience']