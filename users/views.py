from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .forms import UserRegisterForm,PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User   
from .models import FriendRequests,Profile,Posts,Comment,Like
from notifications.signals import notify
# Create your views here.
@login_required
def home(request):
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user 
            form.save()
            return redirect("slide-home")
    else:
        form=PostForm()              
    user_liked_post = []
    posts= Posts.objects.all()
    user_likes=Like.objects.filter(user=request.user)
    for item in user_likes:
        user_liked_post.append(item.post)
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
            if f in users_friends_user_list or f == request.user or FriendRequests.objects.filter(sent_from=request.user,sent_to=f):
                pass
            else:
                friends_suggestion.append(f)
    print(friends_suggestion)
    return render(request,"users/index.html",{"post":posts,"form":form,"user_liked_post":user_liked_post,"friends_suggestion":friends_suggestion})
    
def detailedpost(request,slug,id):
    det_post=get_object_or_404(Posts,pk=id)
    if request.method=="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user 
            form.instance.post= det_post
            form.save()
            return redirect("detailed-post", slug=slug, id=id)
    else:
            form=CommentForm()               
    comments=Comment.objects.filter(post=det_post)
    post_likes=det_post.likes.all()
    user_liked_post=Like.objects.filter(user=request.user,post=det_post).first()
    print(user_liked_post)
    return render(request,"users/detailedpost.html",{"post":det_post,"comments":comments,"post_likes":post_likes,"user_liked_post":user_liked_post,"form":form})    

def profile(request, slug):
    auth_user_friends=request.user.friends_list.all()
    auth_user_friends_users=[]
    users_requests_already_sent=[]
    users_requests_already_recieved=[]
    for item in auth_user_friends:
        auth_user_friends_users.append(item.user)
    req_slug=slug
    user=get_object_or_404(User,username=req_slug)
    profiles_owner=user
#    user=u.user
    friends=user.friends_list.all()
    posts=user.posts.all()
    users_requests_sent_to=FriendRequests.objects.filter(sent_from=request.user)
    users_requests_recieved_from=FriendRequests.objects.filter(sent_to=request.user)
    for item in users_requests_sent_to:
        users_requests_already_sent.append(item.sent_to)
    for item in users_requests_recieved_from:
        users_requests_already_recieved.append(item.sent_from)     
    users_requests=FriendRequests.objects.filter(sent_from=request.user)|FriendRequests.objects.filter(sent_to=request.user).order_by("-time_sent")
    return render(request,"users/profile.html",{"friends":friends,"profiles_owner":profiles_owner,"posts":posts,"auth_user_friends_users":auth_user_friends_users,"users_requests":users_requests,"users_requests_already_sent":users_requests_already_sent,"users_requests_already_recieved":users_requests_already_recieved}
    )
#def suggested_user_list(request):
#    friends_suggestion = []
#    all_users= User.objects.all()
#    friend_requests_sent= FriendRequests.objects.filter(sent_from=request.user)
#    users_friends= request.user.friends_list.exclude(user=request.user)
#    users_friends_user_list = []
#    for friend in users_friends:
#        users_friends_user_list.append(friend.user)
#    print(users_friends_user_list)
#    for friend in users_friends:
#        friends_friend = friend.friends.all()
#        #print(friend,friends_friend)
#        for f in friends_friend:
#            if f in users_friends_user_list or f == request.user:
#                pass
#            else:
#                friends_suggestion.append(f)
#    print(friends_suggestion)
#    return render(request,"users/profile.html",{"friends_suggestion":friends_suggestion,friend_requests_sent:"friend_requests_sent"})

def like_post(request):
    id=request.GET["id"]
    det_post=get_object_or_404(Posts,id=id)         
    like_post=Like.objects.filter(post=det_post,user=request.user)
    print("hiiii")
    if like_post:
        like_post.delete()
        state="not_liked"
    else:
        like_post= Like(post=det_post,user=request.user) 
        like_post.save()
        sender = request.user
        receiver = det_post.user
        notify.send(sender, recipient=receiver, verb="liked post")
        state="liked"
    return HttpResponse(state)

def friend_list(request):
    friends= request.user.friends_list.all()
    return render(request,{"friends","friends"})
    
def send_friend_request(request):
    user=get_object_or_404(User,username=request.GET["username"])
    #pik=request.GET["id"]
    #print(pik)
    f_request=FriendRequests(sent_from=request.user,sent_to=user)
    print(request.user)
    print(user)
    f_request.save()
    return HttpResponse("done")
    
def cancel_friend_request(request):
    user=get_object_or_404(User,username=request.GET["username"])
    print(user)
 #   users_requests=FriendRequests.objects.filter(sent_from=request.user)&FriendRequests.objects.filter(sent_to=user)
    users_requests=FriendRequests.objects.get(sent_from=request.user, sent_to=user)
    users_requests.delete()
    return HttpResponse("done")
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
    
def accept_friend_request(request):
    user1=get_object_or_404(User,username=request.GET["username"])
    request.user.profile.friends.add(user1)
    user1.profile.friends.add(request.user)
    req= FriendRequests.objects.filter(sent_from=user1, sent_to=request.user).delete()
    return HttpResponse("done")
    
def decline_friend_request(request):  
    user1=get_object_or_404(User,username=request.GET["username"])
    req= FriendRequests.objects.filter(sent_from=user1, sent_to=request.user).delete()
    return HttpResponse("done")
  
def register(request):    
    if request.method=="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form=UserRegisterForm ()            
    return render(request,"users/register.html", {"form":form})
    
        