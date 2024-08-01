from rest_framework import serializers
from .models import *




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Roles.objects.all())  

    class Meta:
        model = CustomUser
        fields = ['username', 'password','first_name', 'last_name', 'email','role_id','id']
        depth = 1   

 

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


#----------Custome Token claim--------

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        user_id = refresh.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        access_token = refresh.access_token
        access_token['role_id'] = str(user.role_id) 
        access_token['role_name'] = str(user.role_id.name)
        if user.role_id.name == 'Recruiter':
            try:
                access_token['recruiter_id'] = str(user.recruiters.recruiter_id)
            except:
                access_token['recruiter_id'] = None

        elif user.role_id.name=='Applicant':
            try:
                access_token['Applicant_id'] = str(user.applicants.applicant_id)
            except:
                access_token['Applicant_id'] = None
        elif user.role_id.name =='Admin':
            access_token['Admin_id'] = None
        
        
        data['access'] = str(access_token)
        return data



