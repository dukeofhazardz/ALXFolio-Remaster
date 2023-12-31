from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('<str:github_username>/', views.portfolio, name='portfolio'),
    path('education', views.education, name='education'),
    path('social', views.social, name='social'),
    path('about', views.about, name='about'),
]
