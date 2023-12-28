from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Education, Social


class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    github_username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

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
    school = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    year = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    degree = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Education
        fields = ['school', 'year', 'degree']


class UserSocialForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    whatido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    twitter = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    linkedin = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    instagram = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Social
        fields = ['bio', 'title', 'whatido', 'twitter', 'linkedin', 'instagram']
