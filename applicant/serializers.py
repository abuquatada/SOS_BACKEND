from rest_framework import serializers
from app.models import *
from applicant.models import *
from jobposting.serializers import SkillSerializer,IndustrySerializer,DepartmentSerializer2
from app.serializers import CustomUserSerializer,UserSerializer

class ApplicantSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())  # Or use SerializerMethodField if needed
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), write_only=True)
    interested_industry = serializers.PrimaryKeyRelatedField(many=True, queryset=Industry.objects.all(), write_only=True)
    interested_department = serializers.PrimaryKeyRelatedField(many=True, queryset=Department.objects.all(), write_only=True)
    id = CustomUserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    interested_industry = IndustrySerializer(many=True, read_only=True)
    interested_department = DepartmentSerializer2(many=True, read_only=True)

    class Meta:
        model = Applicants
        fields = '__all__'
        depth = 1

class ApplicantEducationSerializer(serializers.ModelSerializer):
    applicant_id = serializers.PrimaryKeyRelatedField(queryset=Applicants.objects.all())
    applicant_id = ApplicantSerializer()
    class Meta:
        model = ApplicantEducation
        fields = '__all__'

class ApplicantExperienceSerializer(serializers.ModelSerializer):
    applicant_id = serializers.PrimaryKeyRelatedField(queryset=Applicants.objects.all())
    industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all())
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    industry_name = serializers.CharField(source='industry.industry_name', read_only=True)

    class Meta:
        model = ApplicantExperience
        fields = '__all__'
        depth = 1

class ApplicantInternshipSerializer(serializers.ModelSerializer):
    applicant_id = serializers.PrimaryKeyRelatedField(queryset=Applicants.objects.all())
    applicant_id = ApplicantSerializer()
    class Meta:
        model = ApplicantInternship
        fields = '__all__'
        depth = 1

class ApplicantCertificationSerializer(serializers.ModelSerializer):
    applicant_id = serializers.PrimaryKeyRelatedField(queryset=Applicants.objects.all())

    class Meta:
        model = ApplicantCertification
        fields = '__all__'
        depth = 1

class ApplicantSerializer2(serializers.ModelSerializer):
    educations = ApplicantEducationSerializer(many=True, read_only=True)
    experiences = ApplicantExperienceSerializer(many=True, read_only=True)
    internships = ApplicantInternshipSerializer(many=True, read_only=True)
    certifications = ApplicantCertificationSerializer(many=True, read_only=True)

    class Meta:
        model = Applicants
        fields = ['educations', 'experiences', 'internships', 'certifications']

class ApplicantCustomSerializer(serializers.ModelSerializer):
    education = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()
    internship = serializers.SerializerMethodField()
    certification = serializers.SerializerMethodField()

    class Meta:
        model = Applicants
        fields = "__all__"
        depth = 1

    def get_education(self, obj):
        education = ApplicantEducation.objects.filter(applicant_id=obj)
        return ApplicantEducationSerializer(education, many=True).data

    def get_experience(self, obj):
        experience = ApplicantExperience.objects.filter(applicant_id=obj)
        return ApplicantExperienceSerializer(experience, many=True).data

    def get_internship(self, obj):
        internship = ApplicantInternship.objects.filter(applicant_id=obj)
        return ApplicantInternshipSerializer(internship, many=True).data

    def get_certification(self, obj):
        certification = ApplicantCertification.objects.filter(applicant_id=obj)
        return ApplicantCertificationSerializer(certification, many=True).data
    
class Applicant_custom(serializers.ModelSerializer):
    education = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()
    internship = serializers.SerializerMethodField()
    certification = serializers.SerializerMethodField()

    class Meta:
        model = Applicants
        fields = "__all__"
        depth=1

    def get_education(self, obj):
        education = ApplicantEducation.objects.filter(applicant_id=obj)
        return ApplicantEducationSerializer(education, many=True).data

    def get_experience(self, obj):
        experience = ApplicantExperience.objects.filter(applicant_id=obj)
        return ApplicantExperienceSerializer(experience, many=True).data

    def get_internship(self, obj):
        internship = ApplicantInternship.objects.filter(applicant_id=obj)
        return ApplicantInternshipSerializer(internship, many=True).data

    def get_certification(self, obj):
        certification = ApplicantCertification.objects.filter(applicant_id=obj)
        return ApplicantCertificationSerializer(certification, many=True).data
    



