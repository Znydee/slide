from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete = models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image=models.ImageField(default="default.jpg" , upload_to="profile_pictures")
    background_image=models.ImageField(default="default.jpg" , upload_to="profile_pictures")
    email= models.EmailField(blank=True)
    slug = AutoSlugField(populate_from='user',always_update=True)
    friends= models.ManyToManyField(User,related_name="friends_list", blank=True)
    phone=PhoneNumberField(blank=True)
    def __str__(self):
        return f"{self.user.username}'s profile"
class Posts(models.Model):
    user=models.ForeignKey(User,related_name="posts",on_delete=models.CASCADE)       
    post=models.TextField(blank=False)
    date_posted=models.DateTimeField(auto_now_add=True)
    
class FriendRequests(models.Model):
    sent_from = models.ForeignKey(User,related_name="request_sent",on_delete=models.CASCADE)
    sent_to = models.ForeignKey(User,related_name="request_recieved",on_delete=models.CASCADE)
    time_sent= models.            DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"from{self.sent_from.username} to {self.sent_to.username}"
        
class Comment(models.Model):       
    post = models.ForeignKey(Posts,related_name="post_comments",on_delete=models.CASCADE)
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    comment_made = models.TextField(blank=False)
    comment_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f" {self.user.username} commented '{self.comment_made}' on {self.post}"
        
class Like(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="likes")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="post_liked")