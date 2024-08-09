from rest_framework import serializers
from .models import *


class interviwerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Interviewer
        fields='__all__'