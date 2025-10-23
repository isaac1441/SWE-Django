from django import forms
from .models import Post
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=15, label='Username')
    email = forms.EmailField(max_length=30, label='Email')
    password = forms.CharField(max_length=20, label='Password', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        
        allowed_domains = ['gmail.com','yahoo.com','outlook.com', '.edu', 'proton.me']
        domain = email.split('@')[-1].lower()

        if domain not in allowed_domains:
            raise forms.ValidationError(f"Only these domains are allowed: {', '.join(allowed_domains)}")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']        

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already registered.")
        
        return username

class LogInForm(forms.Form):
    identifier = forms.CharField(max_length=50, label='Username or Email')
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields =['title', 'body']