from django.shortcuts import render
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    return render(request,"users/index.html")

def register(request):
    form=UserRegisterForm
    return render(request,"users/register.html", {"form":form})