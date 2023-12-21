from django.contrib import admin
from django.urls import path
from . import views
import dis

urlpatterns = [
    path('', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('education', views.education, name='education'),
    path('social', views.social, name='social'),
]
