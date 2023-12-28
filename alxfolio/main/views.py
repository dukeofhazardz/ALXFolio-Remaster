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
        education_id = custom_user.education_id
        social_id = custom_user.social_id
        education = None
        socials = None

        try:
            education = Education.objects.get(id=education_id)
            socials = Social.objects.get(id=social_id)
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

            education_id = custom_user.education_id
            social_id = custom_user.social_id
            education = None
            socials = None

            try:
                education = Education.objects.get(id=education_id)
                socials = Social.objects.get(id=social_id)
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
            form = UserEducationForm(request.POST, instance=user.education)
            if form.is_valid():
                education_instance = form.save(commit=False)
                education_instance.save()
                return redirect('education')
        else:
            form = UserEducationForm(instance=user.education)
        return render(request, 'education.html', {'form': form})
    messages.error(request, 'You must be logged in to update education.')
    return redirect('login')

def social(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            form = UserSocialForm(request.POST, instance=user.social)
            if form.is_valid():
                social_instance = form.save(commit=False)
                social_instance.save()
                return redirect('social')
        else:
            form = UserSocialForm(instance=user.social)
        return render(request, 'social.html', {'form': form})
    messages.error(request, 'You must be logged in to update social.')
    return redirect('login')
