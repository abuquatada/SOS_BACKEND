from django.contrib import admin
from .models import *

admin.site.register(Interviewer)
admin.site.register(Interview)
admin.site.register(InterviewQuestion)
admin.site.register(InterviewPhase)