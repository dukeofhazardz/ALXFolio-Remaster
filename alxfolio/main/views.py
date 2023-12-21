from django.shortcuts import render, redirect
from django.contrib import messages
from .models import GithubData
from custom_user.forms import UserEducationForm, UserSocialForm
import asyncio

# Create your views here.
def home(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'home.html', {'user': user})
    return render(request, 'home.html')

def profile(request):
    user = request.user
    if user.is_authenticated:
        username = user.github_username
        g = GithubData(username)
        data = asyncio.run(g.get_user())
        repos = asyncio.run(g.get_repos())
        return render(request, 'profile.html', {'user': user, 'data': data, 'repos': repos})
    messages.error(request, 'You must be logged in to view your profile.')
    return redirect('login')

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
            form = UserSocialForm(instance=user.education)
        return render(request, 'social.html', {'form': form})
    messages.error(request, 'You must be logged in to update social.')
    return redirect('login')
