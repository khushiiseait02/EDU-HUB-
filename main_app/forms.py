from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import LearningResource, Organization, ProjectRoom, UserDetails, Post, Event, Hackathon,Job
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    contact_no = forms.CharField(max_length=15, required=False)
    college_name = forms.CharField(max_length=100, required=False)
    domain = forms.CharField(max_length=100, required=False)
    age = forms.IntegerField(required=False)
    profession = forms.CharField(max_length=100, required=False)

    class Meta:
        model = UserDetails
        fields = ['username', 'email', 'contact_no', 'college_name', 'domain', 'age', 'profession', 'password1', 'password2']

class OrganizerRegisterForm(UserCreationForm):
    email = forms.EmailField()
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = UserDetails
        fields = ['username', 'email', 'description', 'password1', 'password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']

class ProjectRoomForm(forms.ModelForm):
    class Meta:
        model = ProjectRoom
        fields = ['title', 'description','required_users']

class LearningResourceForm(forms.ModelForm):
    class Meta:
        model = LearningResource
        fields = ['title', 'description', 'file']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'venue', 'date_time']

class HackathonForm(forms.ModelForm):
    class Meta:
        model = Hackathon
        fields=['title', 'description', 'venue', 'date_time', 'mode']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields=['title', 'description']



