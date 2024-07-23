from rest_framework import serializers
from .models import *
from recruiter.serializers import *





class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class DepartmentSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_id','department_name']

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'


class IndustrySerializer2(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['industry_name']

class CompanySerializer(serializers.ModelSerializer):
    industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all(), many=True)    
    class Meta:    
        model = Company
        fields = '__all__'
        depth = 1

class DepartmentSerializer(serializers.ModelSerializer):
    industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all(), many=True)

    class Meta:
        model = Department
        fields = '__all__'
        # depth = 1

class LocationSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        model = Location
        fields = '__all__'
        depth = 1

class CompanySerializer2(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class IndustrySerializer3(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['industry_id', 'industry_name']

class CompanySerializer3(serializers.ModelSerializer):
    industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all(), many=True)
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['company_id','company_name','phone_number','email','website','industry','founded_date','company_size','logo','description','locations']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['industry'] = IndustrySerializer3(instance.industry.all(), many=True).data
        return representation

    def create(self, validated_data):
        industries_data = validated_data.pop('industry')
        company = Company.objects.create(**validated_data)
        company.industry.set(industries_data)
        return company

    def update(self, instance, validated_data):
        industries_data = validated_data.pop('industry', None)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.website = validated_data.get('website', instance.website)
        instance.founded_date = validated_data.get('founded_date', instance.founded_date)
        instance.company_size = validated_data.get('company_size', instance.company_size)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if industries_data is not None:
            instance.industry.set(industries_data)
        
        return instance

class JobPostingSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), write_only=True)
    industry_id = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all())
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    company_data = CompanySerializer2(read_only=True)
    current_status = serializers.SerializerMethodField()
    location_data = LocationSerializer(read_only=True,source='location')
    department = DepartmentSerializer(read_only=True,source='department_id')
    industry = IndustrySerializer(read_only=True,source='industry_id')
    posted_by = RecruiterSerializer(read_only=True,source='created_by')
    class Meta:
        model = JobPosting
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['company'] = CompanySerializer2(instance.company).data
        return representation

    def get_current_status(self, obj):
        return obj.current_status()
    
class JobStatusLogSerializer2(serializers.ModelSerializer):
    class Meta:
        model = JobStatusLog
        fields = ['status_id']


class JobStatusLogSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(queryset=JobPosting.objects.all())
    status_id = serializers.PrimaryKeyRelatedField(queryset=JobStatus.objects.all())
    class Meta:
        model = JobStatusLog
        fields = '__all__'
        depth = 1
    
class JobPosting2Serializer(serializers.ModelSerializer):
    location =LocationSerializer()
    class Meta:
        model = JobPosting
        fields = '__all__'
        # depth = 1

class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobStatus
        fields = '__all__'




##----------------------

class CSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()