from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserSignupForm


def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user:
            login(request, user)
            messages.success(request, ("You have successfully logged in"))
            return redirect('home')
        else:
            messages.error(request, ("There was an error logging in, Try again"))
            return redirect('login')

    return render(request, 'authenticate/login.html', {})


def user_logout(request):
    logout(request)
    messages.success(request, ("You have successfully logged out"))
    return redirect('home')


def user_signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request, 'authenticate/signup.html', {'form': form})
