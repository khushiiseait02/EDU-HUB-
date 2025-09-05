from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class UserDetails(AbstractUser):
    is_organizer = models.BooleanField(default=False)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    college_name = models.CharField(max_length=100, blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

class Organization(models.Model):
    user = models.OneToOneField(UserDetails, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()

class Job(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.CharField(max_length=200)
    date_time = models.DateTimeField()

class Hackathon(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    mode = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')])

class ProjectRoom(models.Model):
    owner = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_users = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class LearningResource(models.Model):
    uploader = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    domain = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    author = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='posts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JoinRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(ProjectRoom, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'room')

class Notification(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message