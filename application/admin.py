from django.contrib import admin
from .models import * 



admin.site.register(Application)
admin.site.register(ApplicationStatus)
admin.site.register(ApplicationStatusLog)