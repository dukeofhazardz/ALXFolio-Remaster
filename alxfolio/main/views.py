from django.shortcuts import render, redirect
from django.contrib import messages
from .models import GithubData
from custom_user.forms import UserEducationForm, UserSocialForm, CustomUser, Education, Social
from asgiref.sync import async_to_sync

# Create your views here.
def home(request):
    user = request.user
    users = CustomUser.objects.all()
    if user.is_authenticated:
        return render(request, 'home.html', {'user': user, 'users': users})
    return render(request, 'home.html', {'users': users})

def profile(request):
    user = request.user
    if user.is_authenticated:
        username = user.github_username
        g = GithubData(username)

        get_user_sync = async_to_sync(g.get_user)
        get_repos_sync = async_to_sync(g.get_repos)

        data = get_user_sync()
        repos = get_repos_sync()

        custom_user = CustomUser.objects.get(github_username=username)
        user_id = custom_user.id
        education = None
        socials = None

        try:
            education = Education.objects.get(user_id=user_id)
            socials = Social.objects.get(user_id=user_id)
        except Education.DoesNotExist:
            education = None
        except Social.DoesNotExist:
            socials = None

        return render(request, 'profile.html', {'user': user,
                                                'data': data,
                                                'repos': repos,
                                                'education': education,
                                                'socials': socials})
    messages.error(request, 'You must be logged in to view your profile.')
    return redirect('home')

def portfolio(request, github_username=None):
    if github_username is not None and github_username != '':
        try:
            custom_user = CustomUser.objects.get(github_username=github_username)
            g = GithubData(github_username)
        
            get_user_sync = async_to_sync(g.get_user)
            get_repos_sync = async_to_sync(g.get_repos)

            data = get_user_sync()
            repos = get_repos_sync()

            user_id = custom_user.id
            education = None
            socials = None

            try:
                education = Education.objects.get(user_id=user_id)
                socials = Social.objects.get(user_id=user_id)
            except Education.DoesNotExist:
                education = None
            except Social.DoesNotExist:
                socials = None

            return render(request, 'portfolio.html', {'data': data,
                                                      'repos': repos,
                                                      'education': education,
                                                      'socials': socials})
        
        except CustomUser.DoesNotExist:
            return render(request, '404.html')
    return render(request, '404.html')

def education(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            form = UserEducationForm(request.POST)
            if form.is_valid():
                education_instance = form.save(commit=False)
                education_instance.user = request.user
                education_instance.save()
                messages.success(request, 'Education Update Successful')
                return redirect('education')
        else:
            form = UserEducationForm()
        return render(request, 'education.html', {'form': form})
    messages.error(request, 'You must be logged in to update education.')
    return redirect('login')

def social(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            form = UserSocialForm(request.POST)
            if form.is_valid():
                social_instance = form.save(commit=False)
                social_instance.user = request.user
                social_instance.save()
                messages.success(request, 'Socials Update Successful')
                return redirect('social')
        else:
            form = UserSocialForm()
        return render(request, 'social.html', {'form': form})
    messages.error(request, 'You must be logged in to update social.')
    return redirect('login')
