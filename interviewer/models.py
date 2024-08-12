from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from application.models import Application 

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


class Interview(models.Model):
    interview_id=models.AutoField(primary_key=True)
    application_id=models.ForeignKey(Application,on_delete=models.CASCADE)
    phase=models.CharField(max_length=100)
    type=models.CharField(max_length=100,choices=[
        ('Onsite','Onsite'),
        ('Virtual','Virtual'),
    ],default='Onsite')
    scheduled_date=models.DateField(blank=True,null=True)
    interviewer =models.ForeignKey(Interviewer,on_delete=models.CASCADE)
    location=models.CharField(max_length=100)
    virtual_link=models.URLField(max_length=100)
    status=models.CharField(max_length=100)
    notes=models.CharField(max_length=100)

