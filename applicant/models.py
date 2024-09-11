from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from jobposting.models import *
from app.models import CustomUser

class Applicants(models.Model):        
    applicant_id = models.AutoField(primary_key=True)
    profile_photo = models.ImageField(upload_to='applicant_documents/',null=True,blank=True)
    id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True,blank=True)
    phone_number = PhoneNumberField()
    martial_status = models.CharField(max_length=30)
    home_town = models.CharField(max_length=100)
    permanent_address = models.CharField(max_length=255)
    pincode = models.IntegerField()
    current_location = models.CharField(max_length=400)
    skills = models.ManyToManyField (Skill)
    resume = models.FileField(upload_to="media/applicant_resume")
    preferred_job_type = models.CharField(max_length=100)
    preferred_location = models.CharField(max_length=255)
    total_years_of_experience = models.PositiveIntegerField(null=True,blank=True)
    interested_industry = models.ManyToManyField(Industry)
    interested_department = models.ManyToManyField(Department)
    availability_to_join = models.CharField(max_length=20)  
    work_permit_for_USA = models.BooleanField(default=False)
    languages = models.CharField(max_length=255, blank=True,null = True)
    about = models.CharField(null=True,max_length=1000)

class ApplicantEducation(models.Model):  
    applicant_id = models.ForeignKey(Applicants, on_delete=models.CASCADE,related_name='educations')
    degree = models.CharField(max_length=100)
    field_of_specialization = models.CharField(max_length=200, blank=True)
    institute_name = models.CharField(max_length=200)
    date_of_completion= models.DateField()
    
    def __str__(self):
        return self.degree

class ApplicantExperience(models.Model):
    # applicant_experience_id=models.AutoField(primary_key=True)     
    applicant_id = models.ForeignKey(Applicants, on_delete=models.CASCADE,related_name='experiences')    
    company_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    salary = models.IntegerField(null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.company_name

class ApplicantInternship(models.Model):  
    applicant_id = models.ForeignKey(Applicants, on_delete=models.CASCADE,related_name='internships')
    company_name = models.CharField(max_length=100)
    position_title = models.CharField(max_length=50)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    internship_certificate = models.FileField(upload_to="media/applicant_internship",null=True, blank=True)
    
    def __str__(self):
        return self.company_name

class ApplicantCertification(models.Model):  
    applicant_id = models.ForeignKey(Applicants, on_delete=models.CASCADE,related_name='certifications')
    certification_name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    certifcate = models.FileField(upload_to="media/applicant_certificates",null = True,blank=True)
    
    def __str__(self):
        return self.certification_name
    



class Applicant_Document(models.Model):
    document_id=models.AutoField(primary_key=True)
    applicant_id=models.ForeignKey(Applicants,on_delete=models.CASCADE)
    job_id=models.ForeignKey(JobPosting,on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    document=models.FileField(null=True,blank=True)
    verified=models.CharField(max_length=100, choices=[
        ("pending","pending"),
        ("unverified","unverified"),
        ("verified","verified")
    ],default="pending")