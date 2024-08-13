from rest_framework import serializers
from .models import *
from application.serializers import Application2Serializer


class interviwerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Interviewer
        fields='__all__'
       


class interviewSerializer(serializers.ModelSerializer):
    application_id=serializers.PrimaryKeyRelatedField(queryset=Application.objects.all())
    interviewer=serializers.PrimaryKeyRelatedField(queryset=Interviewer.objects.all())
    class Meta:
        model=Interview
        fields='__all__'
        depth=1
        

class InterviewPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=InterviewPhase
        fields='__all__'
        

class InterviewQuestionSerializer(serializers.ModelSerializer):
    phase = InterviewPhaseSerializer()
    class Meta:
        model=InterviewQuestion
        fields='__all__'