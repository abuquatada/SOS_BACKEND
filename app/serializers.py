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


