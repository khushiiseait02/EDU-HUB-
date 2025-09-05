from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from .forms import EventForm, HackathonForm, JobForm, LearningResourceForm, PostForm, ProjectRoomForm, UserRegisterForm, OrganizerRegisterForm
from .models import JoinRequest, Notification, Organization, Job, Event, Hackathon, Post, ProjectRoom, LearningResource
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from .models import UserDetails
from django.contrib import messages
from django.views.decorators.http import require_POST

from django.contrib.auth import get_user_model

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # Assuming is_staff is used to differentiate organizers
            user.save()
            login(request, user)
            return redirect('user_home')
    else:
        form = UserRegisterForm()
    return render(request, 'register_user.html', {'form': form})

def register_organizer(request):
    if request.method == 'POST':
        form = OrganizerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Assuming is_staff is used to differentiate organizers
            user.save()
            Organization.objects.create(user=user, description=form.cleaned_data.get('description'))
            login(request, user)
            return redirect('organizer_home')
    else:
        form = OrganizerRegisterForm()
    return render(request, 'register_organizer.html', {'form': form})

@login_required
def user_home(request):
    return render(request, 'user_home.html')


@login_required
def search_job(request):
    jobs = Job.objects.all()
    return render(request, 'search_job.html', {'jobs': jobs})

@login_required
def search_job_orgs(request):
    jobs = Job.objects.all()
    return render(request, 'search_job_orgs.html', {'jobs': jobs})

@login_required
def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

@login_required
def events_orgs(request):
    events = Event.objects.all()
    return render(request, 'events_orgs.html', {'events': events})


login_required
def hackathons(request):
    hackathons = Hackathon.objects.all()
    return render(request, 'hackathons.html', {'hackathons': hackathons})

login_required
def hackathons_org(request):
    hackathons = Hackathon.objects.all()
    return render(request, 'hackathons_org.html', {'hackathons': hackathons})


# @login_required
# def project_collab(request):
#     project_rooms = ProjectRoom.objects.all()
#     return render(request, 'project_collab.html', {'project_rooms': project_rooms})
@login_required
def project_collab(request):
    user = request.user
    project_rooms = ProjectRoom.objects.all()

    project_rooms_with_requests = []
    for room in project_rooms:
        join_request_exists = JoinRequest.objects.filter(user=user, room=room).exists()
        project_rooms_with_requests.append({
            'room': room,
            'join_request_exists': join_request_exists,
            'is_owner': room.owner == user
        })

    context = {
        'project_rooms_with_requests': project_rooms_with_requests
    }

    return render(request, 'project_collab.html', context)


@login_required
@require_POST
def send_join_request(request):
    user = request.user
    room_id = request.POST.get('room_id')
    room = ProjectRoom.objects.get(id=room_id)

    if not JoinRequest.objects.filter(user=user, room=room).exists():
        JoinRequest.objects.create(user=user, room=room)

    return redirect('project_collab')


@login_required
def create_project_room(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        required_users = request.POST.get('required_users')
        
        # Ensure the owner is the logged-in user
        ProjectRoom.objects.create(owner=request.user, title=title, description=description, required_users=required_users)
        
        return redirect('project_collab')  # Redirect to project collaboration page after creation
    
    return render(request, 'create_project_room.html')


@login_required
def learn_upload(request):
    if request.method == 'POST':
        title = request.POST['title']
        domain = request.POST['domain']
        description = request.POST['description']
        file = request.FILES['file']
        
        # Ensure the uploader is the logged-in user
        uploader = request.user
        
        # Create the LearningResource instance
        LearningResource.objects.create(uploader=uploader, title=title, domain=domain, description=description, file=file)
        if(uploader.is_staff==1):
            return redirect('organizer_home')
        else:
            return redirect('user_home')  # Redirect to the search page after upload
    
    return render(request, 'learn_upload.html')

@login_required
def learn_upload_orgs(request):
    if request.method == 'POST':
        title = request.POST['title']
        domain = request.POST['domain']
        description = request.POST['description']
        file = request.FILES['file']
        
        # Ensure the uploader is the logged-in user
        uploader = request.user
        
        # Create the LearningResource instance
        LearningResource.objects.create(uploader=uploader, title=title, domain=domain, description=description, file=file)
        if(uploader.is_staff==1):
            return redirect('organizer_home')
        else:
            return redirect('user_home')  # Redirect to the search page after upload
    
    return render(request, 'learn_upload_orgs.html')


@login_required
def learn_search(request):
    resources = LearningResource.objects.all()
    return render(request, 'learn_search.html', {'resources': resources})

@login_required
def learn_search_org(request):
    resources = LearningResource.objects.all()
    return render(request, 'learn_search_org.html', {'resources': resources})



@login_required
def organize_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        venue = request.POST.get('venue')
        date_time = request.POST.get('date_time')
        Event.objects.create(organization=request.user.organization, title=title, description=description, venue=venue, date_time=date_time)
        return redirect('organizer_home')
    return render(request, 'organize_event.html')


@login_required
def organize_hackathon(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        venue = request.POST.get('venue')
        date_time = request.POST.get('date_time')
        mode = request.POST.get('mode')
        Hackathon.objects.create(organization=request.user.organization, title=title, description=description, venue=venue, date_time=date_time, mode=mode)
        return redirect('organizer_home')
    return render(request, 'organize_hackathon.html')


@login_required
def post_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Job.objects.create(organization=request.user.organization, title=title, description=description)
        return redirect('organizer_home')
    return render(request, 'post_job.html')


def main_home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST.get('user_type')  # Assuming there's a form field to specify user type
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print({user})
            print('is staff: ')
            print({user.is_staff})
            if user_type == 'organizer' and user.is_staff:  # Check if user is an organizer
                return redirect('organizer_home')  # Redirect to organizer home page
            elif user.is_staff==0 and user_type=='normal':
                print("user login")
                return redirect('user_home')
            else:
                return render(request, 'main_home.html', {'error': 'Invalid credentials'})
            
        else:
            return render(request, 'main_home.html', {'error': 'Invalid credentials'})
    return render(request, 'main_home.html')



@login_required
def user_home(request):
    query = request.GET.get('query', '')

    # Initialize the search results dictionary
    results = {
        'jobs': [],
        'events': [],
        'hackathons': [],
        'projects': [],
        'resources': [],
        'posts': []
    }

    if query:
        # Perform search for each type of item
        results['jobs'] = Job.objects.filter(title__icontains=query) | Job.objects.filter(description__icontains=query)
        results['events'] = Event.objects.filter(title__icontains=query) | Event.objects.filter(description__icontains=query)
        results['hackathons'] = Hackathon.objects.filter(title__icontains=query) | Hackathon.objects.filter(description__icontains=query)
        results['projects'] = ProjectRoom.objects.filter(title__icontains=query) | ProjectRoom.objects.filter(description__icontains=query)
        results['resources'] = LearningResource.objects.filter(title__icontains=query) | LearningResource.objects.filter(description__icontains=query)
        results['posts'] = Post.objects.filter(title__icontains=query) | Post.objects.filter(description__icontains=query)

    
    return render(request, 'user_home.html', {'results': results})

@login_required
def organizer_home(request):
    query = request.GET.get('query', '')

    # Initialize the search results dictionary
    results = {
        'jobs': [],
        'events': [],
        'hackathons': [],
        'projects': [],
        'resources': [],
        'posts': []
    }

    if query:
        # Perform search for each type of item
        results['jobs'] = Job.objects.filter(title__icontains=query) | Job.objects.filter(description__icontains=query)
        results['events'] = Event.objects.filter(title__icontains=query) | Event.objects.filter(description__icontains=query)
        results['hackathons'] = Hackathon.objects.filter(title__icontains=query) | Hackathon.objects.filter(description__icontains=query)
        results['projects'] = ProjectRoom.objects.filter(title__icontains=query) | ProjectRoom.objects.filter(description__icontains=query)
        results['resources'] = LearningResource.objects.filter(title__icontains=query) | LearningResource.objects.filter(description__icontains=query)
        results['posts'] = Post.objects.filter(title__icontains=query) | Post.objects.filter(description__icontains=query)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('organizer_home')
    else:
        form = PostForm()
    return render(request, 'organizer_home.html', {'results': results, 'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('user_home')  # or 'organizer_home'
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def create_post_org(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('organizer_home')  # or 'organizer_home'
    else:
        form = PostForm()
    return render(request, 'create_post_org.html', {'form': form})

@login_required
def view_posts(request):
    posts = Post.objects.all()
    return render(request, 'view_posts.html', {'posts': posts})

@login_required
def view_posts_org(request):
    posts = Post.objects.all()
    return render(request, 'view_posts_org.html', {'posts': posts})


@login_required
def logout(request):
    django_logout(request)
    return redirect('main_home')

@login_required
def profile_view(request, username):
    user = get_object_or_404(UserDetails, username=username)
    return render(request, 'profile.html', {'user': user})


@login_required
def my_activity(request):
    posts = Post.objects.filter(author=request.user)
    project_rooms = ProjectRoom.objects.filter(owner=request.user)
    resources = LearningResource.objects.filter(uploader=request.user)
    
    activities = []
    for post in posts:
        activities.append({
            'type': 'post',
            'instance': post
        })
    for project_room in project_rooms:
        activities.append({
            'type': 'project_room',
            'instance': project_room
        })
    for resource in resources:
        activities.append({
            'type': 'resource',
            'instance': resource
        })
    

    context = {
        'activities': activities,
    }
    return render(request, 'my_activity.html', context)


@login_required
def my_activity_org(request):
    # Ensure the user is an organizer
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('user_home')

    # Fetch the organization related to the logged-in user
    organization = get_object_or_404(Organization, user=request.user)

    posts = Post.objects.filter(author=request.user)
    project_rooms = ProjectRoom.objects.filter(owner=request.user)
    resources = LearningResource.objects.filter(uploader=request.user)
    events = Event.objects.filter(organization=organization)
    hackathons = Hackathon.objects.filter(organization=organization)
    jobs = Job.objects.filter(organization=organization)

    activities = []
    for post in posts:
        activities.append({
            'type': 'post',
            'instance': post
        })
    for project_room in project_rooms:
        activities.append({
            'type': 'project_room',
            'instance': project_room
        })
    for resource in resources:
        activities.append({
            'type': 'resource',
            'instance': resource
        })
    for event in events:
        activities.append({
            'type': 'event',
            'instance': event
        })
    for hackathon in hackathons:
        activities.append({
            'type': 'hackathon',
            'instance': hackathon
        })
    for job in jobs:
        activities.append({
            'type': 'job',
            'instance': job
        })

    context = {
        'activities': activities,
    }
    return render(request, 'my_activity_org.html', context)


@login_required
def edit_activity(request, activity_type, activity_id):
    # Determine the form and model based on activity_type
    if activity_type == 'post':
        model = Post
        form_class = PostForm
    elif activity_type == 'project_room':
        model = ProjectRoom
        form_class = ProjectRoomForm
    elif activity_type == 'resource':
        model = LearningResource
        form_class = LearningResourceForm
    elif activity_type == 'event':
        model = Event
        form_class = EventForm
    elif activity_type == 'hackathon':
        model = Hackathon
        form_class = HackathonForm
    elif activity_type == 'job':
        model = Job
        form_class = JobForm
    else:
        # Handle invalid activity type
        messages.error(request, "Invalid activity type.")
        if request.user.is_staff:
            return redirect('my_activity_org')
        else:
            return redirect('my_activity')

    # Fetch the object to edit
    instance = get_object_or_404(model, id=activity_id)

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity updated successfully!")
            if request.user.is_staff:
                return redirect('my_activity_org')
            else:
                return redirect('my_activity')
        else:
            messages.error(request, "Error updating activity.")
    else:
        form = form_class(instance=instance)

    context = {
        'form': form,
        'activity_type': activity_type
    }
    return render(request, 'edit_activity.html', context)


@login_required
def delete_activity(request, activity_id, activity_type):
    # Determine the model based on activity_type
    if activity_type == 'post':
        model = Post
    elif activity_type == 'project_room':
        model = ProjectRoom
    elif activity_type == 'resource':
        model = LearningResource
    elif activity_type == 'event':
        model = Event
    elif activity_type == 'hackathon':
        model = Hackathon
    elif activity_type == 'job':
        model = Job
    else:
        messages.error(request, "Invalid activity type.")
        if request.user.is_staff:
            return redirect('my_activity_org')
        else:
            return redirect('my_activity')

    # Fetch the object to delete
    instance = get_object_or_404(model, id=activity_id)

    if request.method == 'POST':
        instance.delete()
        messages.success(request, "Activity deleted successfully!")
        if request.user.is_staff:
            return redirect('my_activity_org')
        else:
            return redirect('my_activity')
    else:
        messages.error(request, "Invalid request method.")
        if request.user.is_staff:
            return redirect('my_activity_org')
        else:
            return redirect('my_activity')


@login_required
def view_join_requests(request):
    requests = JoinRequest.objects.filter(room__owner=request.user, is_accepted=False)
    return render(request, 'view_join_requests.html', {'requests': requests})

@login_required
def join_project_room(request, room_id):
    room = get_object_or_404(ProjectRoom, id=room_id)
    
    # Prevent room owner from sending a join request
    if room.owner == request.user:
        messages.error(request, 'You cannot join your own room.')
        return redirect('project_collaboration')
    
    # Prevent users from sending multiple requests
    join_request, created = JoinRequest.objects.get_or_create(user=request.user, room=room)
    if not created:
        messages.error(request, 'You have already sent a request to join this room.')
    else:
        messages.success(request, 'Your request to join the project room has been sent.')
    
    return redirect('project_collaboration')

# @login_required
# def handle_join_request(request, request_id, action):
#     join_request = get_object_or_404(JoinRequest, id=request_id, room__owner=request.user)
    
#     if action == 'accept':
#         join_request.is_accepted = True
#         join_request.save()
#         join_request.room.required_users -= 1
#         join_request.room.save()
#         messages.success(request, f'You have accepted {join_request.user} into the project room.')
#     elif action == 'reject':
#         join_request.delete()
#         messages.success(request, f'You have rejected {join_request.user} from the project room.')
    
#     return redirect('view_join_requests')

@login_required
def handle_join_request(request, request_id, action):
    user = request.user
    join_request = JoinRequest.objects.get(id=request_id)

    if action == 'accept':
        join_request.is_accepted = True
        join_request.room.required_users -= 1
        join_request.room.save()
        message = f"Your join request for '{join_request.room.title}' has been accepted."
    elif action == 'reject':
        join_request.is_accepted = False
        message = f"Your join request for '{join_request.room.title}' has been rejected."

    join_request.save()

    # Create a notification for the user
    Notification.objects.create(user=join_request.user, message=message)

    return redirect('view_join_requests') 

@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')

    # Mark all notifications as read
    notifications.update(is_read=True)

    context = {
        'notifications': notifications
    }

    return render(request, 'notifications.html', context)