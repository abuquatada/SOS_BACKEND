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

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    newpassword = serializers.CharField()



##----------------------

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        access_token = refresh.access_token
        user_id = refresh['user_id']
        try:
            user = CustomUser.objects.get(id=user_id)
            access_token['role'] = str(user.role_id)
        except CustomUser.DoesNotExist:
            pass

        data['access'] = str(access_token)
        return data