from rest_framework import serializers
from .models import *
from jobposting.serializers import *
from applicant.serializers import *

class ApplicationSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(queryset=JobPosting.objects.all())
    applicant_id = serializers.PrimaryKeyRelatedField(queryset=Applicants.objects.all())
    company_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    referral_id = serializers.PrimaryKeyRelatedField(queryset=Recruiters.objects.all())
    job = JobPostingSerializer(read_only=True, source='job_id')
    applicant = ApplicantSerializer(read_only=True, source='applicant_id')
    company = CompanySerializer(read_only=True, source='company_id')
    referral = RecruiterSerializer(read_only=True, source='referral_id')
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        latest_log = ApplicationStatusLog.objects.filter(application_id=obj).order_by('-date_changed').first()
        return latest_log.status_id.status_name if latest_log else None
    
    class Meta:
        model = Application
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        application = super().create(validated_data)
        print(application)
        job_posting = application.job_id
        job_posting.application_count += 1
        job_posting.save()
        return application



class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = '__all__'  
             

class ApplicationStatusLogSerializer(serializers.ModelSerializer):
    # status_id = serializers.PrimaryKeyRelatedField(queryset=ApplicationStatus.objects.all())
    application_id = serializers.PrimaryKeyRelatedField(queryset=Application.objects.all())
    class Meta:
        model = ApplicationStatusLog
        fields = '__all__' 
        depth = 1

class Application2Serializer(serializers.ModelSerializer):
    # job_id = serializers.PrimaryKeyRelatedField(queryset=JobPosting.objects.all())
    # applicant_id = serializers.PrimaryKeyRelatedField(queryset=Applicants.objects.all())
    # company_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    # referral_id = serializers.PrimaryKeyRelatedField(queryset=Recruiters.objects.all())
    job_id = JobPosting2Serializer()
    application_status_log = serializers.SerializerMethodField()
    

    class Meta:
        model = Application
        fields = '__all__'
        depth = 2
    
    def get_application_status_log(self, obj):
        log = ApplicationStatusLog.objects.filter(application_id=obj)
        return ApplicationStatusLogSerializer(log, many=True).data
