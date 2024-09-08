from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from app.models import *
from jobposting.models import *

 

class   Recruiters(models.Model):    
    recruiter_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    companies = models.ManyToManyField(Company)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True)
    phone_number = PhoneNumberField()
    martial_status = models.CharField(max_length=30)
    home_town = models.CharField(max_length=100)
    permanent_address = models.CharField(max_length=255)
    pincode = models.IntegerField()
    current_location = models.CharField(max_length=400)
    resume = models.FileField(upload_to="media/recruiter_resumes")
    total_years_of_experience = models.PositiveIntegerField(null=True,blank=True)
    languages = models.CharField(max_length=255, blank=True,null = True)
    about = models.CharField(null=True,max_length=1000)
    profile_photo = models.ImageField(upload_to="media/profile_photos_recruiters", null=True, blank=True)


class RecruiterEducation(models.Model):  
    recruiter_id = models.ForeignKey(Recruiters, on_delete=models.CASCADE,related_name='educations')
    degree = models.CharField(max_length=100)
    field_of_specialization = models.CharField(max_length=200, blank=True)
    institute_name = models.CharField(max_length=200)
    date_of_completion= models.DateField()


class RecruiterExperience(models.Model):     
    recruiter_id = models.ForeignKey(Recruiters, on_delete=models.CASCADE,related_name='experiences')    
    company_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    salary = models.IntegerField(null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)


class RecruiterCertification(models.Model):  
    recruiter_id = models.ForeignKey(Recruiters, on_delete=models.CASCADE,related_name='certifications')
    certification_name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    certifcate = models.FileField(upload_to="media/recruiter_certificates",null=True, blank=True)

class Recruiter_Specific_Job(models.Model):
    recruiter_Specific_Job_id = models.AutoField(primary_key=True)
    job_id=models.ForeignKey(JobPosting,on_delete=models.CASCADE,null=True)
    recruiter_id = models.ForeignKey(Recruiters,on_delete=models.CASCADE,null=True)

class EmployeeLog(models.Model):
    emplog_id=models.AutoField(primary_key=True)
    recruiter_id=models.ForeignKey('Recruiters', on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    activity_time=models.DateTimeField(auto_now_add=True)
    remarks=models.CharField(max_length=1000)
    activity_type=models.CharField(max_length=500)
    
    def total_work_hours(self):
        if self.activity_type == 'logout':
            login_log = EmployeeLog.objects.filter(
                recruiter_id=self.recruiter_id,
                activity_type='login',
                date=self.date
            ).last()
            if login_log:
                return (self.activity_time - login_log.activity_time).seconds // 3600
        return 0

