from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.db import models


class CustomUser(BaseUser):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    github_username = models.CharField(max_length=100, null=False, unique=True)
    phone_no = models.CharField(max_length=15, null=False)
    address = models.CharField(max_length=100, null=False)
    
    objects = BaseUserManager()

    def __str__(self):
        return self.email


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


class Education(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='education')
    school = models.CharField(max_length=100, null=True)
    year = models.CharField(max_length=100, null=True)
    degree = models.CharField(max_length=100, null=True)

class Social(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='social')
    bio = models.CharField(max_length=500, null=True)
    title = models.CharField(max_length=100, null=True)
    whatido = models.CharField(max_length=500, null=True)
    twitter = models.CharField(max_length=100, null=True)
    linkedin = models.CharField(max_length=100, null=True)
    instagram = models.CharField(max_length=100, null=True)
