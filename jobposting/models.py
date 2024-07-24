from django.db import models
from phonenumber_field.modelfields import PhoneNumberField





class Company(models.Model):     
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True,null=True)
    industry = models.ManyToManyField('Industry')
    founded_date = models.DateField(blank=True, null=True)
    company_size = models.IntegerField(blank=True, null=True)
    logo = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.company_name

class Location(models.Model):  
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE,related_name='locations')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

class Industry(models.Model):           
    industry_id = models.AutoField(primary_key=True)
    industry_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.industry_name


class Department(models.Model):      
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    industry = models.ManyToManyField('Industry')
     
    def __str__(self):
        return self.department_name

class Skill(models.Model):   
    skill_id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100)

    def __str__(self):
        return self.skill_name


class JobStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.status_name

class JobPosting(models.Model):   
    job_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    job_position = models.CharField(max_length=100)
    industry_id = models.ForeignKey(Industry, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=100) #Full Time, Permanent
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    benefits = models.TextField(blank=True)
    salary = models.IntegerField(null=True, blank=True)
    location_type = models.CharField(max_length=20, choices=[
        ('Onsite', 'Onsite'),
        ('Remote', 'Remote'),
    ], default='Onsite') 
    location = models.ForeignKey(Location, on_delete=models.CASCADE)    
    application_deadline = models.DateTimeField()
    application_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    application_count = models.IntegerField(default=0,null=True,blank=True)

    def current_status(self):
        latest_log = JobStatusLog.objects.filter(job_id=self).order_by('-date_changed').first()
        return latest_log.status_id.status_name if latest_log else None

class JobStatusLog(models.Model):
    joblog_id = models.AutoField(primary_key=True)
    job_id = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    status_id = models.ForeignKey(JobStatus, on_delete=models.CASCADE)
    date_changed = models.DateTimeField(auto_now_add=True)





