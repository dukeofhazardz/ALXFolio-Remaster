from django.shortcuts import render, redirect
from django.contrib import messages
from .models import GithubData
from custom_user.forms import UserEducationForm, UserSocialForm, CustomUser, Education, Social
from asgiref.sync import async_to_sync


def home(request):
    user = request.user
    users = CustomUser.objects.all()
    if user.is_authenticated:
        return render(request, 'home.html', {'user': user, 'users': users})
    return render(request, 'home.html', {'users': users})


def about(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'about.html', {'user': user})
    return render(request, 'about.html', {})


def portfolio(request, github_username):
    user = None
    try:
        current_user = request.user
        if current_user.is_authenticated:
            username = current_user.github_username
            if username == github_username:
                user = current_user
    except Exception as err:
        print(err)

    try:
        g = GithubData(github_username)

        get_user_sync = async_to_sync(g.get_user)
        get_repos_sync = async_to_sync(g.get_repos)

        data = get_user_sync()
        repos = get_repos_sync()

        custom_user = CustomUser.objects.get(github_username=github_username)
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
        bio = socials.bio or None
        whatido = socials.whatido or None
        title = socials.title or None
        twitter = socials.twitter or None
        instagram = socials.instagram or None
        linkedin = socials.linkedin or None
        social = [instagram, twitter, linkedin]
        return render(request, 'portfolio.html', {'user': user,
                                                'data': data,
                                                'repos': repos,
                                                'education': education,
                                                'bio': bio,
                                                'whatido': whatido,
                                                'title': title,
                                                'socials': social})
    except CustomUser.DoesNotExist:
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
