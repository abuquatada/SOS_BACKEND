from django.db import models
from applicant.models import Applicants
from recruiter.models import *


class Application(models.Model):
    application_id = models.AutoField(primary_key=True)
    applicant_id = models.ForeignKey(Applicants, on_delete=models.CASCADE)
    job_id = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    referral_id = models.ForeignKey(Recruiters, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.applicant_id.id.first_name
    
class ApplicationStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100)

    def __str__(self):
        return self.status_name

class ApplicationStatusLog(models.Model):
    applog_id = models.AutoField(primary_key=True)
    application_id = models.ForeignKey(Application, on_delete=models.CASCADE)
    status_id = models.ForeignKey(ApplicationStatus, on_delete=models.CASCADE)
    date_changed = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.status_id.status_name
