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

    def __str__(self):
        return f"Interview {self.interview_id} for Application {self.application_id}"
    
class InterviewPhase(models.Model):
    phase_id=models.AutoField(primary_key=True)
    phase_name=models.CharField(max_length=100)
    
class InterviewQuestion(models.Model):
    question_id=models.AutoField(primary_key=True)
    phase=models.ForeignKey(InterviewPhase,on_delete=models.CASCADE)
    question_text=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.BigIntegerField()