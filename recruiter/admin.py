from django.contrib import admin
from .models import *




admin.site.register(Company)
admin.site.register(Location)
admin.site.register(Industry)
admin.site.register(Department)
admin.site.register(Skill)
admin.site.register(JobPosting)
admin.site.register(JobStatus)
admin.site.register(JobStatusLog)
admin.site.register(Recruiter_Specific_Job)
admin.site.register(RecruiterCertification)
admin.site.register(RecruiterEducation)
admin.site.register(RecruiterExperience)
admin.site.register(Recruiters)