from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms  import UserCreationForm
from .models import Profile,Posts,Comment
from phonenumber_field.widgets import PhoneNumberPrefixWidget

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
        widgets = {
            'phone': PhoneNumberPrefixWidget(),
        }
        fields=["profile_image","background_image","bio","phone"]
        

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["comment_made"]
        labels={"comment_made":""}
                
class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["post"]
        labels={"post":""}
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        
        self.fields['post'].widget.attrs['placeholder'] = 'Write Something Cool!'
