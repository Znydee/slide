from django.shortcuts import render
from .forms import UserRegisterForm
# Create your views here.
def home(request):
    form=UserRegisterForm
    return render(request,"users/index.html", {"form":form})