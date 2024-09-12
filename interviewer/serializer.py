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
    feedback = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Interview
        fields='__all__'
        
    def get_phase_details(self, obj):
        phase_obj = InterviewPhase.objects.get(phase_interview=obj)
        return InterviewPhaseSerializer(phase_obj).data    
    def get_interviewer_details(self, obj):
        interviewer_obj = Interviewer.objects.get(interview_interviewer=obj)
        return InterviewerSerializer(interviewer_obj).data
    def get_feedback(self,obj):
        try :
             feedback_obj = Interview_feedback.objects.get(Interview=obj)
             return Interview_feedback_Serializer(feedback_obj).data    
        except:
            return []     
                

class InterviewQuestionSerializer(serializers.ModelSerializer):
    phase_name = serializers.CharField(source='phase.phase_name',read_only=True)
    class Meta:
        model=InterviewQuestion
        fields='__all__'
 
 
class Interview_feedback_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Interview_feedback
        fields = "__all__" 
        
class Google_formSerializer(serializers.ModelSerializer):
    class Meta:
        model = Google_form
        fields = "__all__" 






        
               