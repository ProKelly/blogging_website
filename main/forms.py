from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django import forms  
from django.contrib.auth.models import User
from .models import BlogPost, Comments

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
        ]
   
        
class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'author', 'content']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']