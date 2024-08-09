from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Interviewer(models.Model):
    Interviewer_id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField()
    gender=models.CharField(max_length=100)
    date_of_birth=models.DateField(blank=True,null=True)
    phone_number=PhoneNumberField()
    total_years_of_experience=models.IntegerField()
    language=models.CharField(max_length=100)
    about=models.CharField(max_length=100)

