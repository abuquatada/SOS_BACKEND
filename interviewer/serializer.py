from rest_framework import serializers
from .models import *
from application.serializers import *


class InterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Interviewer
        fields='__all__'
       
class InterviewPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=InterviewPhase
        fields='__all__'
   
class InterviewSerializer(serializers.ModelSerializer):
    phase_details = serializers.SerializerMethodField(read_only=True)
    interviewer_details = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model=Interview
        fields='__all__'
        
    def get_phase_details(self, obj):
        phase_obj = InterviewPhase.objects.get(phase_interview=obj)
        return InterviewPhaseSerializer(phase_obj).data    
    def get_interviewer_details(self, obj):
        interviewer_obj = Interviewer.objects.get(interview_interviewer=obj)
        return InterviewerSerializer(interviewer_obj).data    
                

class InterviewQuestionSerializer(serializers.ModelSerializer):
    phase = InterviewPhaseSerializer()
    class Meta:
        model=InterviewQuestion
        fields='__all__'
 
 
class Interview_feedback_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Interview_feedback
        feilds = "__all__" 
        