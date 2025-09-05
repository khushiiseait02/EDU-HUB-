from django.contrib import admin
from .models import UserDetails, Organization, Job, Event, Hackathon, ProjectRoom, LearningResource

admin.site.register(UserDetails)
admin.site.register(Organization)
admin.site.register(Job)
admin.site.register(Event)
admin.site.register(Hackathon)
admin.site.register(ProjectRoom)
admin.site.register(LearningResource)



