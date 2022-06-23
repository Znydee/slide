from django.shortcuts import render, redirect,get_object_or_404
from .forms import UserRegisterForm,PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User   
from .models import FriendRequests,Profile
# Create your views here.
@login_required
def home(request):
    return render(request,"users/index.html")

def profile(request, slug):
    req_slug=slug
    user=get_object_or_404(User,username=req_slug)
#    user=u.user
    friends=user.friends_list.all()
    return render(request,"users/profile.html",{"friends":friends}
    )
def suggested_user_list(request):
    friends_suggestion = []
    all_users= User.objects.all()
    friend_requests_sent= FriendRequests.objects.filter(sent_from=request.user)
    users_friends= request.user.friends_list.exclude(user=request.user)
    users_friends_user_list = []
    for friend in users_friends:
        users_friends_user_list.append(friend.user)
    print(users_friends_user_list)
    for friend in users_friends:
        friends_friend = friend.friends.all()
        #print(friend,friends_friend)
        for f in friends_friend:
            if f in users_friends_user_list or f == request.user:
                pass
            else:
                friends_suggestion.append(f)
    print(friends_suggestion)
    return render(request,"users/profile.html",{"friends_suggestion":friends_suggestion,friend_requests_sent:"friend_requests_sent"})
    
def friend_list(request):
    friends= request.user.friends_list.all()
    return render(request,{"friends","friends"})
    
def send_friend_request(request,id):
    user=get_object_or_404(User,pk=id)
    f_request=friendReuqests(sent_from=request.user,sent_to=user)
    f_request.save()
    return redirect("slide-home")

def make_post(request):
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user 
            form.save()
            return redirect("slide-home")
    else:
        form=PostForm()      
    return render(request,"users/make_post.html", {"form":form})
    
def accept_friend_request(request,id):
    user1=get_or_404(User,pk=id)
    request.user.friends_list.add(user1)
    user1.profile.friends.add(request.user)
    return redirect("slide-home")
     
def register(request):    
    if request.method=="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form=UserRegisterForm ()            
    return render(request,"users/register.html", {"form":form})