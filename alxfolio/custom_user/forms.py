from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Education, Social


class UserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'github_username', 'password1', 'password2', 'phone_no', 'address']

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with this email already exists')
            return email
        
        def clean_username(self):
            username = self.clean_data.get('username')
            if CustomUser.objects.filter(username=username).exists():
                raise forms.ValidationError('A user with this username already exists')
            return username


class UserEducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'year', 'degree']


class UserSocialForm(forms.ModelForm):
    class Meta:
        model = Social
        fields = ['bio', 'title', 'whatido', 'twitter', 'linkedin', 'instagram']
