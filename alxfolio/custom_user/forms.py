from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Education, Social


class UserEducationForm(forms.ModelForm):
    school = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'School'}))
    year = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Year'}))
    degree = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Degree'}))

    class Meta:
        model = Education
        fields = ['school', 'year', 'degree']


class UserSocialForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Bio'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Title'}))
    whatido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'What You Do'}))
    twitter = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Twitter'}))
    linkedin = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'LinkedIn'}))
    instagram = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Instagram'}))

    class Meta:
        model = Social
        fields = ['bio', 'title', 'whatido', 'twitter', 'linkedin', 'instagram']


class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    github_username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Github Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirm Password'}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address (State, Country)'}))
    
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
