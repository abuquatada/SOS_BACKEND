import django_filters
from .models import *


class InterviewQuestionFilter(django_filters.FilterSet):
    phase = django_filters.CharFilter(field_name='phase__phase_name' ,  lookup_expr='icontains')

    class Meta:
        model = InterviewQuestion
        fields = ['phase']
