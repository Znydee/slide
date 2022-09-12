from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .forms import UserRegisterForm,PostForm,CommentForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User   
from .models import FriendRequests,Profile,Posts,Comment,Like
from notifications.signals import notify
import notifications
from django.utils.timesince import timesince
from django.core.paginator import Paginator
# Create your views here.
@login_required
def home(request):
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user 
            reciever_list=[]
            sender = request.user
            reciever = list(request.user.friends_list.all().values("user_id"))  
            for item in reciever:
                reciever_list.append((User.objects.get(id=item['user_id'])))                        
            form.save()
            notify.send(sender, recipient=reciever_list, verb='new post')
            return redirect("slide-home")
    else:
        form=PostForm()              
    user_liked_post = []
    #posts= Posts.objects.all().order_by("-pk")
    
    #paginator = Paginator(posts, 5,orphans=4)
#    page_number = request.GET.get('page')
#    page_obj = paginator.get_page(page_number)
    user_likes=Like.objects.filter(user=request.user)
    for item in user_likes:
        user_liked_post.append(item.post)
    friends_suggestion = []
    all_users= User.objects.all()
    friend_requests_sent= FriendRequests.objects.filter(sent_from=request.user)
    users_friends= request.user.friends_list.exclude(user=request.user)
    users_friends_user_list = [request.user.username]
    users_friends_user_id_list = [request.user.id]
    friend_suggestion_list=[]
    for friend in users_friends:
        users_friends_user_list.append(friend.user.username)
        users_friends_user_id_list.append(friend.user.id)
    friends_suggestion= User.objects.exclude(username__in=users_friends_user_list)
    users_requests_already_sent=[]
    users_requests_already_recieved=[]
    users_requests_sent_to=FriendRequests.objects.filter(sent_from=request.user)
    users_requests_recieved_from=FriendRequests.objects.filter(sent_to=request.user)
    for item in users_requests_sent_to:
        users_requests_already_sent.append(item.sent_to)
    for item in users_requests_recieved_from:
        users_requests_already_recieved.append(item.sent_from)     
    users_requests=FriendRequests.objects.filter(sent_from=request.user)|FriendRequests.objects.filter(sent_to=request.user).order_by("-time_sent")
    print(users_friends_user_id_list)
    posts = Posts.objects.filter(user_id__in = users_friends_user_id_list).order_by("-date_posted")
    print(posts.count())
    paginator = Paginator(posts,10,orphans=4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #for item in all_users:
#        if item in users_friends_user_list :
#            all_users.exclude(item)
#    friends_suggestion= all_users
    
#    for friend in users_friends:
#        friends_friend = friend.friends.all()
#        for f in friends_friend:
#            if f in users_friends_user_list or f == request.user or FriendRequests.objects.filter(sent_from=request.user,sent_to=f):
#                pass
#            else:
#                friends_suggestion.append(f)
    return render(request,"users/index.html",{"page_obj":page_obj,"form":form,"user_liked_post":user_liked_post,"friends_suggestion":friends_suggestion,"users_requests":users_requests,"users_requests_already_sent":users_requests_already_sent,"users_requests_already_recieved":users_requests_already_recieved})

def get_all_notifications(request):
    all_notifications=request.user.notifications.all()
    all_notifications=list(all_notifications.values())
    for item in all_notifications:
        timesince_format=timesince(item["timestamp"])
        item["timesince_format"]=timesince_format    
    return JsonResponse(all_notifications, safe=False)

def notifications_as_read(request):
    #print(request.user.notifications.all())
    notif = request.user.notifications.exclude(verb="new message")&request.user.notifications.exclude(verb="new post")
    #print(notif)
    notif.mark_all_as_read()       
    return HttpResponse("done")
def detailedpost(request,slug,id):
    det_post=get_object_or_404(Posts,pk=id)
    if request.method=="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user 
            form.instance.post= det_post
            form.save()
            sender = request.user
            receiver = det_post.user
            notify.send(sender, recipient=receiver, verb="comment on post", description=f"{sender.username} commented on your post",rel_obj_content=det_post.post)
            return redirect("detailed-post", slug=slug, id=id)
    else:
            form=CommentForm()               
    comments=Comment.objects.filter(post=det_post)
    post_likes=det_post.likes.all()
    user_liked_post=Like.objects.filter(user=request.user,post=det_post).first()
    return render(request,"users/detailedpost.html",{"post":det_post,"comments":comments,"post_likes":post_likes,"user_liked_post":user_liked_post,"form":form})    

def profile(request, slug):
    auth_user_friends=request.user.friends_list.all()
    auth_user_friends_users=[]
    users_requests_already_sent=[]
    users_requests_already_recieved=[]
    user_liked_post = []
    users_likes= request.user.post_liked.all()
    for item in users_likes:
        user_liked_post.append(item.post)
    for item in auth_user_friends:
        auth_user_friends_users.append(item.user)
    req_slug=slug
    user=get_object_or_404(User,username=req_slug)
    profiles_owner=user
    profiles_owner_bio=get_object_or_404(Profile,user=profiles_owner)
    friends=user.friends_list.all()
    posts=user.posts.all()
    users_requests_sent_to=FriendRequests.objects.filter(sent_from=request.user)
    users_requests_recieved_from=FriendRequests.objects.filter(sent_to=request.user)
    for item in users_requests_sent_to:
        users_requests_already_sent.append(item.sent_to)
    for item in users_requests_recieved_from:
        users_requests_already_recieved.append(item.sent_from)     
    users_requests=FriendRequests.objects.filter(sent_from=request.user)|FriendRequests.objects.filter(sent_to=request.user).order_by("-time_sent")
    return render(request,"users/profile.html",{"friends":friends,"profiles_owner":profiles_owner,"profiles_owner_bio":profiles_owner_bio,"posts":posts,"auth_user_friends_users":auth_user_friends_users,"users_requests":users_requests,"users_requests_already_sent":users_requests_already_sent,"users_requests_already_recieved":users_requests_already_recieved,
"users_likes":users_likes,
"user_liked_post":user_liked_post
}
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
    request.user.notifications.filter(data={"rel_obj_content":det_post.post}).delete()
    if like_post:
        like_post.delete()
            
        state="not_liked"
    else:
        like_post= Like(post=det_post,user=request.user) 
        like_post.save()
        sender = request.user
        receiver = det_post.user
        notify.send(sender, recipient=receiver, verb="like post", description=f"{sender.username} liked your post",rel_obj_content=det_post.post)
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
            users_name = request.POST["username"]
            users_email=request.POST["email"]
            user_obj= User.objects.get(username= users_name)
            Profile.objects.create(user=user_obj,email=users_email)
            return redirect("login")
    else:
        form=UserRegisterForm()            
    return render(request,"users/register.html", {"form":form})
    
def profileupdate(request):        
    instance=  Profile.objects.filter(user=request.user).first()
    if request.method=="POST":        
        form = ProfileUpdateForm(request.POST, request.FILES, instance = instance )
        if form.is_valid():            
            form.save()
            return redirect("profile", slug=instance.user.username)
    else:
        form = ProfileUpdateForm(instance = instance )
    return render(request,"users/profileupdate.html", {"form":form})        
    
        