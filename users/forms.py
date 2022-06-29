from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms  import UserCreationForm
from .models import Profile,Posts

class UserRegisterForm(UserCreationForm):
    email= forms.EmailField()
    class Meta:
        model = User
        fields=["username","email","password1","password2"]

class UserUpdateForm(forms.ModelForm):
    email= forms.EmailField()
    class Meta:
        model=User
        fields=["username","email"]
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["image","bio"]
        
class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["post"]
        labels={"post":""}
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        
        self.fields['post'].widget.attrs['placeholder'] = 'Write Something Cool!'
