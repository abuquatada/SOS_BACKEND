from rest_framework import serializers
from .models import *
from app.serializers import UserSerializer

class RecruiterSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())  # Or use SerializerMethodField if needed
    user_id =UserSerializer(read_only=True)
    class Meta:
        model = Recruiters
        fields = '__all__'
        depth = 1

class RecruiterEducationSerializer(serializers.ModelSerializer):
    recruiter_id = serializers.PrimaryKeyRelatedField(queryset=Recruiters.objects.all())

    class Meta:
        model = RecruiterEducation
        fields = '__all__'
        depth = 1


class RecruiterExperienceSerializer(serializers.ModelSerializer):
    recruiter_id = serializers.PrimaryKeyRelatedField(queryset=Recruiters.objects.all())

    class Meta:
        model = RecruiterExperience
        fields = '__all__'
        depth = 1


class RecruiterCertificationSerializer(serializers.ModelSerializer):
    recruiter_id = serializers.PrimaryKeyRelatedField(queryset=Recruiters.objects.all())

    class Meta:
        model = RecruiterCertification
        fields = '__all__'
        depth = 1

class RecruiterSerializer2(serializers.ModelSerializer):
    educations = RecruiterEducationSerializer(many=True, read_only=True)
    experiences = RecruiterExperienceSerializer(many=True, read_only=True)
    certifications = RecruiterCertificationSerializer(many=True, read_only=True)

    class Meta:
        model = Recruiters
        fields = ['educations', 'experiences', 'certifications']    
    
class Recruiter2Serializer(serializers.ModelSerializer):
    education = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()
    # internship = serializers.SerializerMethodField()
    certification = serializers.SerializerMethodField()
    user_id = UserSerializer()
    class Meta:
        model = Recruiters
        fields = '__all__'
        # depth = 1    
    
    
    def get_education(self, obj):
        education = RecruiterEducation.objects.filter(recruiter_id=obj)
        return RecruiterEducationSerializer(education, many=True).data

    def get_experience(self, obj):
        experience = RecruiterExperience.objects.filter(recruiter_id=obj)
        return RecruiterExperienceSerializer(experience, many=True).data

    def get_certification(self, obj):
        certification = RecruiterCertification.objects.filter(recruiter_id=obj)
        return RecruiterCertificationSerializer(certification, many=True).data
    

class Recruiter_Specific_JobSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recruiter_Specific_Job
        fields = '__all__' 
 
class Recruiter_Specific_Job2Serializer(serializers.ModelSerializer):
    recruiter_id=serializers.PrimaryKeyRelatedField(queryset=Recruiters.objects.all())
    # job_id=serializers.PrimaryKeyRelatedField(queryset=JobPosting.objects.all())
    class Meta:
        model = Recruiter_Specific_Job
        fields = '__all__' 
        depth=2 
        

class EmployeeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=EmployeeLog
        fields='__all__'